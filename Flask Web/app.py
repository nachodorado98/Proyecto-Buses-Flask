#Importamos la libreria Flask
from flask import Flask, render_template, url_for, request, redirect
#Importamos la clase ConsultaBuses para hacer las consultas
from consultas_bbdd import ConsultaBuses

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
@app.route("/agregarlinea", methods=["GET", "POST"])
def agregar_linea():

	#Obtenemos las lineas no recorridas llamando a la funcion lineas
	lineas_no_recorridas=ConsultaBuses.lineas(0)

	#Damos formato a las lineas
	unidas=["Linea: "+i[0]+" Inicio: "+i[1]+" Fin: "+i[2] for i in lineas_no_recorridas]

	#Devolvemos el template de agregar una linea y le pasamos las lineas no recorridas con el formato
	return render_template("agregar_linea.html", unidas=unidas)


#Funcion para agregar la linea nueva
@app.route("/agregarexito", methods=["GET", "POST"])
def agregar_exito():

	#Obtenemos el numero de la linea que se quiere agregar
	linea=request.form.get("linea").split(" ")[1]

	#Agregamos (actualizamos) la linea
	ConsultaBuses.actualizar_linea(linea)

	#Redireccionamos a la pagina de inicio
	return redirect(url_for("inicio"))


#Si cumple la condicion entra y corre la aplicacion
if __name__=="__main__":

	app.run(debug=True)