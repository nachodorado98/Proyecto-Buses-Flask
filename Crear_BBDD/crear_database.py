from config import Config
from consultas_crear_bbdd import BaseDatos, Tabla, Registros
import os

#Creamos la conexion con MySQL
conexion=Config.crear_conexion()
bbdd=conexion[0]
c=conexion[1]



#--------------------------------------------BASE DE DATOS---------------------------------------
nombre_bbdd="autobuses"
creacion_bbdd=BaseDatos(nombre_bbdd, bbdd, c)
creacion_bbdd.crear_bbdd()


#--------------------------------------------TABLA LINEAS-----------------------------------------
tabla_lineas=Tabla("lineas", nombre_bbdd, bbdd, c)
consulta_tabla_lineas="""CREATE TABLE lineas
						(Linea VARCHAR(20),
						Inicio VARCHAR(60),
						Fin VARCHAR(60),
						Tipo VARCHAR(15),
						FechaInicio DATE,
						FechaFin DATE,
						Recorrida BOOl DEFAULT 0,
						PRIMARY KEY (Linea))"""
creacion_tabla_lineas=tabla_lineas.crear_tabla(consulta_tabla_lineas)

consulta_insertar_lineas="""INSERT INTO lineas
						VALUES(%s, %s, %s, %s, %s, %s, %s)"""
archivo_lineas=os.path.join(os.path.abspath(os.getcwd()), r"Limpiar Tablas\descripcion_lineas_bus")
insertar_tabla_lineas=tabla_lineas.insertar_datos(consulta_insertar_lineas, Registros.csv_lista_lineas(archivo_lineas))


#--------------------------------------------TABLA PARADAS-----------------------------------------
tabla_paradas=Tabla("paradas", nombre_bbdd, bbdd, c)
consulta_tabla_paradas="""CREATE TABLE paradas
						(CodParada INT,
						Parada INT,
						Nombre VARCHAR(50),
						Linea VARCHAR(20),
						Sentido VARCHAR(20),
						Latitud FLOAT,
						Longitud FLOAT,
						PRIMARY KEY (CodParada),
						FOREIGN KEY (Linea) REFERENCES lineas (Linea) ON DELETE CASCADE)"""
creacion_tabla_paradas=tabla_paradas.crear_tabla(consulta_tabla_paradas)

consulta_insertar_paradas="""INSERT INTO paradas
						VALUES(%s, %s, %s, %s, %s, %s, %s)"""
archivo_paradas=os.path.join(os.path.abspath(os.getcwd()), r"Limpiar Tablas\paradas_buses")
insertar_tabla_paradas=tabla_paradas.insertar_datos(consulta_insertar_paradas, Registros.csv_lista_paradas(archivo_paradas))
