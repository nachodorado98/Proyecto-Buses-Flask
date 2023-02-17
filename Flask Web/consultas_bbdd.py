#Importamos la clase Config para la configiracion de MySQL
from config import Config

#Creamos la clase ConsultaBuses
class ConsultaBuses():

	#Creamos la conexion
	conexion=Config.crear_conexion()
	bbdd=conexion[0]
	c=conexion[1]

	#Funcion para obtener las lineas segun las quieras recorridas (1) o no (0)
	@staticmethod
	def lineas(recorridas_o_no):
		
		ConsultaBuses.c.execute("""USE autobuses""")
		ConsultaBuses.c.execute("""SELECT Linea, Inicio, Fin
									FROM lineas 
									WHERE Recorrida=%s
									AND Tipo!="Bus Navidad"
									ORDER BY Tipo""",
									(recorridas_o_no,))

		return ConsultaBuses.c.fetchall()

	#Funcion para actualizar una linea en concreto a recorrida
	@staticmethod
	def actualizar_linea(linea):
		ConsultaBuses.c.execute("""USE autobuses""")
		ConsultaBuses.c.execute("""UPDATE lineas
									SET Recorrida=1
									WHERE Linea=%s""",
									(linea,))
		
		ConsultaBuses.bbdd.commit()
		return True

	#Funcion para obtener el detalle de la linea
	@staticmethod
	def detalle_linea(linea):
		ConsultaBuses.c.execute("""USE autobuses""")
		ConsultaBuses.c.execute("""SELECT Inicio, Fin, Tipo, FechaInicio, FechaFin
									FROM lineas 
									WHERE Linea=%s""",
									(linea,))
		
		return ConsultaBuses.c.fetchone()

	#Funcion para obtener las paradas de las lineas que no son favoritas
	@staticmethod
	def paradas_linea(linea):
		ConsultaBuses.c.execute("""USE autobuses""")
		ConsultaBuses.c.execute("""SELECT CodParada, Parada, Nombre, Sentido
									FROM paradas
									WHERE Linea=%s
									AND Favorita=0
									ORDER BY Sentido""",
									(linea,))
		
		return ConsultaBuses.c.fetchall()

	#Funcion para actualizar una parada en favorita
	@staticmethod
	def actualizar_parada_favorita(codparada):
		ConsultaBuses.c.execute("""USE autobuses""")
		ConsultaBuses.c.execute("""UPDATE paradas
									SET Favorita=1
									WHERE CodParada=%s""",
									(codparada,))
		
		ConsultaBuses.bbdd.commit()
		return True


	#Funcion para obtener las paradas favoritas en orden de linea y sentido
	@staticmethod
	def paradas_favoritas_orden():
		ConsultaBuses.c.execute("""USE autobuses""")
		ConsultaBuses.c.execute("""SELECT Parada, Linea, Sentido, Latitud, Longitud
									FROM paradas
									WHERE Favorita=1
									ORDER BY Linea, Sentido""")
		
		return ConsultaBuses.c.fetchall()





	
