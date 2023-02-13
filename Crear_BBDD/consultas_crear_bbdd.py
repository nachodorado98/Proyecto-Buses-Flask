import pandas as pd 

#Clase para crear la Base de datos
class BaseDatos():

	def __init__(self, nombre_bbdd, bbdd, cursor):
		self.nombre_bbdd=nombre_bbdd
		self.bbdd=bbdd
		self.cursor=cursor

	#Crear la BBDD
	def crear_bbdd(self):
		self.cursor.execute(f"DROP DATABASE IF EXISTS {self.nombre_bbdd}")
		self.cursor.execute(f"CREATE DATABASE {self.nombre_bbdd}")

#Clase para crear las tablas	
class Tabla():
	
	def __init__(self, nombre, nombre_bbdd, bbdd, cursor):
		self.nombre=nombre
		self.nombre_bbdd=nombre_bbdd
		self.bbdd=bbdd
		self.cursor=cursor

	#Crear la tabla
	def crear_tabla(self, consulta):
		self.cursor.execute(f"USE {self.nombre_bbdd}")
		self.cursor.execute(f"DROP TABLE IF EXISTS {self.nombre}")
		self.cursor.execute(consulta)
		return True

	#Insertar datos en la tabla
	def insertar_datos(self, consulta, datos):
		self.cursor.execute(f"USE {self.nombre_bbdd}")
		for i in datos:
			self.cursor.execute(consulta, tuple(i))
			self.bbdd.commit()
		return True


#clas para obtener las lineas para insertar en la tabla
class Registros():

	#Funcion para devolver las lineas de csv a una lista
	@staticmethod
	def csv_lista_lineas(csv):
		lista_lineas=pd.read_csv(csv+".csv").values.tolist()
		#Iteramos para modificar la fecha de inicio y de fin a otro formato
		for i in lista_lineas:
			fecha_inicio=i[4].strip().split("/")
			i[4]=fecha_inicio[2]+"/"+fecha_inicio[1]+"/"+fecha_inicio[0]
			fecha_fin=i[5].strip().split("/")
			i[5]=fecha_fin[2]+"/"+fecha_fin[1]+"/"+fecha_fin[0]
			#Agregamos 0 por defecto para el campo recorrido
			i.append(0)
		return lista_lineas

	#Funcion para devolver las paradas de csv a una lista
	@staticmethod
	def csv_lista_paradas(csv):
		lista_paradas=pd.read_csv(csv+".csv").values.tolist()
		#Iteramos para sumar 1 al codigo de la parada (que en realidad es el codigo de cada registro) y convertir a string las lineas
		for i in lista_paradas:
			i[0]=i[0]+1
			i[3]=str(i[3])
		return lista_paradas