#Importamos mysql para poder trabajar con la base de datos
import mysql.connector

class Config():

	#Creamos una funcion para la conexion con mysql
	@staticmethod
	def crear_conexion():
		#Creamos la conexion con mysql
		bbdd=mysql.connector.connect(host="localhost", user="root", passwd="root")
		#Creamos un cursor
		c=bbdd.cursor(buffered=True)
		return bbdd, c 