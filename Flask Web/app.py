#Importamos la libreria Flask
from flask import Flask, render_template, url_for, request, redirect
#Importamos la clase ConsultaBuses para hacer las consultas
from consultas_bbdd import ConsultaBuses
from datetime import datetime
import datetime

#Creamos la aplicacion
app=Flask(__name__)

#Funcion para la pagina de inicio
@app.route("/")
def inicio():

	#Obtenemos las lineas recorridas llamando a la funcion lineas
	lineas_recorridas=ConsultaBuses.lineas(1)

	#Devolvemos el template base y le pasamos las lineas recorridas
	return render_template("base.html", lineas_recorridas=lineas_recorridas)

#Funcion para la pagina de agregar una nueva linea recorrida
@app.route("/agregarlinea/", methods=["GET", "POST"])
def agregar_linea():

	#Obtenemos las lineas no recorridas llamando a la funcion lineas
	lineas_no_recorridas=ConsultaBuses.lineas(0)

	#Damos formato a las lineas
	unidas=["Linea: "+i[0]+" Inicio: "+i[1]+" Fin: "+i[2] for i in lineas_no_recorridas]

	#Devolvemos el template de agregar una linea y le pasamos las lineas no recorridas con el formato
	return render_template("agregar_linea.html", unidas=unidas)


#Funcion para agregar la linea nueva
@app.route("/agregarexito/", methods=["GET", "POST"])
def agregar_exito():

	#Obtenemos el numero de la linea que se quiere agregar
	linea=request.form.get("linea").split(" ")[1]

	#Agregamos (actualizamos) la linea llamando a actualizar_linea
	ConsultaBuses.actualizar_linea(linea)

	#Redireccionamos a la pagina de inicio
	return redirect(url_for("inicio"))

#Funcion para obtener el detalle de una linea
@app.route("/detallelinea<linea>/", methods=["GET", "POST"])
def detalle_linea(linea):

	#Obtenemos el detalle de la linea llamando a detalle_linea
	detalle_linea=ConsultaBuses.detalle_linea(linea)
	inicio=detalle_linea[0]
	fin=detalle_linea[1]
	tipo=detalle_linea[2]
	fecha_inicio=detalle_linea[3].strftime("%d-%m-%Y")

	#Si la fecha de fin es mayor a la actual ponemos que esta en activo
	if detalle_linea[4]>datetime.date.today():
		fecha_fin="En Activo"
	#Si es menor ponemos la fecha de fin
	else:
		fecha_fin=detalle_linea[4].strftime("%d-%m-%Y")

	#Devolvemos el template del detalle de la linea con los datos necesarios
	return render_template("detalle_linea.html", 
							linea=linea, 
							inicio=inicio, 
							fin=fin,
							tipo=tipo,
							fecha_inicio=fecha_inicio,
							fecha_fin=fecha_fin)

#Funcion para selccionar una parada como favorita
@app.route("/detallelinea<linea>/seleccionarparada/", methods=["GET", "POST"])
def seleccionar_parada(linea):

	#Obtenemos las paradas que no son favoritas
	paradas_linea=ConsultaBuses.paradas_linea(linea)

	#Devolvemos el template de la selccion de la parada como favorita
	return render_template("seleccionar_parada.html", linea=linea, paradas_linea=paradas_linea)


#Funcion para agregar la parada como favorita
@app.route("/detallelinea<linea>/seleccionarparada/exito/", methods=["GET", "POST"])
def parada_exito(linea):

	#Obtenemos el codigo de la parada seleccionada
	codigo_parada=request.form.get("parada")

	#Agregamos (actualizamos) la parada
	ConsultaBuses.actualizar_parada_favorita(codigo_parada)

	#Redireccionamos a la pagina de inicio
	return redirect(url_for("inicio"))

#Funcion para la pagina de visualizar las paradas favoritas
@app.route("/paradasfavoritas/")
def paradas_favoritas():

	#Obtenemos las paradas favoritas en orden de linea y sentido
	favoritas=ConsultaBuses.paradas_favoritas_orden()

	#Devolvemos el template de las paradas favoritas y le pasamos las paradas
	return render_template("paradas_favoritas.html", favoritas=favoritas)

#Si cumple la condicion entra y corre la aplicacion
if __name__=="__main__":

	app.run(debug=True)