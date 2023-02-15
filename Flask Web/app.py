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

	#Agregamos (actualizamos) la linea
	ConsultaBuses.actualizar_linea(linea)

	#Redireccionamos a la pagina de inicio
	return redirect(url_for("inicio"))


@app.route("/detallelinea<linea>/", methods=["GET", "POST"])
def detalle_linea(linea):

	detalle_linea=ConsultaBuses.detalle_linea(linea)

	inicio=detalle_linea[0]
	fin=detalle_linea[1]
	tipo=detalle_linea[2]
	fecha_inicio=detalle_linea[3].strftime("%d-%m-%Y")

	if detalle_linea[4]>datetime.date.today():
		fecha_fin="En Activo"
	else:
		fecha_fin=detalle_linea[4].strftime("%d-%m-%Y")

	return render_template("detalle_linea.html", 
							linea=linea, 
							inicio=inicio, 
							fin=fin,
							tipo=tipo,
							fecha_inicio=fecha_inicio,
							fecha_fin=fecha_fin)

#Si cumple la condicion entra y corre la aplicacion
if __name__=="__main__":

	app.run(debug=True)