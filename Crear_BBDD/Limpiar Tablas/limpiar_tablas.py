#Importamos pandas
import pandas as pd
#Importamos os
import os
#Importamos pyproj
import pyproj

#Obtenemos los archivos Excel a leer
lista_archivos=[i for i in os.listdir(os.path.join(os.getcwd(),"Originales")) if i.endswith("xlsx")]


#---------------------------------------------------------LINEAS
#Leemos el Excel de las lineas con pandas 
lineas=pd.read_excel(lista_archivos[0])

#Tiramos la columna de los numeros de las lineas (ya que queremos la de label)
lineas.drop(["Line"], axis=1, inplace=True)

#Rellenamos el valor missing de la navidad
lineas["NameB"].fillna("BUS DE LA NAVIDAD", inplace=True)

#Reemplazamos la denominacion de los tipos de autobuses
lineas["GroupNumber"].replace({110:"Diario", 410:"Diario", 320:"Nocturno", 120:"Trabajo", 210:"Universitario", 155:"Mini", 171:"SE", 160:"SE",420:"Nocturno", 620:"Bus Navidad"}, inplace=True)

#Cambiamos el nombre de las columnas
lineas.rename({"GroupNumber":"Tipo","DateFirst":"FechaInicio","DateEnd":"FechaFin","Label":"Linea","NameA":"Inicio","NameB":"Fin"}, axis=1, inplace=True)

#Establecemos el indice en la columna de las lineas
lineas.set_index("Linea", inplace=True)

#Obtenemos el dataframe con el orden de las columnas que queremos
lineas=lineas[["Inicio","Fin", "Tipo", "FechaInicio", "FechaFin"]]

#Obtenemos una lista con todas las lineas
lista_lineas=lineas.index.to_list()

#Pasamos el dataframe a un CSV
lineas.to_csv("descripcion_lineas_bus.csv")


#---------------------------------------------------------PARADAS
#Leemos el Excel de las paradas con pandas 
paradas=pd.read_excel(lista_archivos[1])

lista_final=[]

#Iteramos por las columnas de las paradas (Nodes) y las lineas (Lines) para luego poder juntarlas al dataframe de nuevo
for i in paradas[["Node","Lines"]].values.tolist():
    #Dividimos por espacios
    split_espacio=i[1].split(" ")
    #Si la lista division tiene mas de un elemento la debemos separar en varios registros por linea
    if len(split_espacio)>1:
        lista=[[i[0], j]for j in split_espacio]
        #Iteramos para dividir por slash
        for m in lista:
            split_slash=m[1].split("/")
            #Lo agregamos a la lista
            lista_final.append([i[0],split_slash[0],split_slash[1]])
            
    #Si no, dividimos por slash
    else:
        split_slash=i[1].split("/")
        #Lo agregamos a la lista
        lista_final.append([i[0],split_slash[0],split_slash[1]])
 

#Obtenemos un pequeño dataframe con la parada, la linea y su sentido
df_lineas_cut=pd.DataFrame(lista_final, columns=["Node","Linea","Sentido"])

#Hacemos join por el campo parada (Node) para juntar el dataframe original y el dividido
df_unido=df_lineas_cut.merge(paradas, on="Node", how="left")

#Reemplazamos la denominacion de los sentidos de las lineas
df_unido["Sentido"].replace({"1":"Ida","2":"Vuelta"},inplace=True)

#Eliminamos la columna linea original ya que tenemos las lineas divididas y sus sentidos
df_unido.drop(["Lines"], axis=1, inplace=True)

#Renombramos las columnas
df_unido.rename({"Node":"Parada","PosxNode":"X", "PosyNode":"Y", "Name":"Nombre"}, axis=1, inplace=True)

#Cambiamos la , por el . en la columna de X y lo pasamos a tipo float
df_unido["X"]=df_unido["X"].str.replace(",",".")
df_unido["X"].astype(float)

#Cambiamos la columna Y a tipo float
df_unido["Y"].astype(float)

#Funcion para pasar las coordenadas x e y a latutud y longitud
def xy_lonlat(lista):
    x=lista[0]
    y=lista[1]
    proj_latlon = pyproj.Proj(proj='latlong',datum='WGS84')
    proj_xy = pyproj.Proj(proj="utm", zone=30, datum='WGS84')
    lonlat = pyproj.transform(proj_xy, proj_latlon, x, y)
    return [lonlat[1], lonlat[0]]

#Creamos una lista con las coordenadas x e y pasadas a latitud y longitud
lista_long_lat=[xy_lonlat(i) for i in df_unido[["X","Y"]].values.tolist()]

#Agregamos una columna con las latitudes
df_unido["Latitud"]=[i[0] for i in lista_long_lat]

#Agregamos una columna con las longitudes
df_unido["Longitud"]=[i[1] for i in lista_long_lat]

#Obtenemos el dataframe con las columnas que queremos
df_unido=df_unido[["Parada", "Nombre", "Linea", "Sentido", "Latitud", "Longitud"]]

#Quitamos las paradas que no estan en la lista de las lineas y reseteamos el indice
df_unido=df_unido[df_unido["Linea"].isin(lista_lineas)].reset_index()

#Eliminamos la columna indice que se crea al resetear el indice
df_unido.drop("index", axis=1, inplace=True)

#Pasamos el dataframe a un CSV
df_unido.to_csv("paradas_buses.csv")





