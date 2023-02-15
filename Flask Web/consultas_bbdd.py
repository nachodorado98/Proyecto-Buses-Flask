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
									WHERE Recorrida=%s""",
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

	@staticmethod
	def detalle_linea(linea):
		ConsultaBuses.c.execute("""USE autobuses""")
		ConsultaBuses.c.execute("""SELECT Inicio, Fin, Tipo, FechaInicio, FechaFin
									FROM lineas 
									WHERE Linea=%s""",
									(linea,))
		
		return ConsultaBuses.c.fetchone()





	
