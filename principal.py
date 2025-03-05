from flask import Flask,render_template,request, redirect, send_from_directory
import mysql.connector
from datetime import datetime
baseDatos=mysql.connector.connect(host="localhost",
                                port="3306",
                                user="root",
                                password="",
                                database="programa2")
programa=Flask(__name__)

@programa.route("/login")
def login ():
    return render_template("login.html")

@programa.route("/comprobar", methods=["POST"])
def comprobar ():
    usuario = request.form["usuario"]
    contraseña=request.form["contraseña"]
    cursor1=baseDatos.cursor()
    sql = f"SELECT * FROM usuarios WHERE usuario='{usuario}'"
    cursor1.execute(sql)
    resultado = cursor1.fetchall()
    if len(resultado) == 1:
        if resultado[0][1] == contraseña:
            ahora = datetime.now()
            fecha = ahora.strftime("%Y%m%d%H%M%S")
            print(fecha)
            return f"hola"
        else :
            return render_template("login.html",usuarios = usuario,contraseñas = contraseña, mensaje_error = "usuario o contraseña incorrectos")
    else:
        return render_template("login.html",usuarios = usuario,contraseñas = contraseña,mensaje_error = "usuario o contraseña incorrectos")


@programa.route ("/registrar")
def registrarse ():
    return render_template("register.html")


@programa.route("/registrarse", methods=["POST"])
def registrar ():
    usuario = request.form["usuario"]
    celular = request.form["celular"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]
    confirmacion = request.form["confirmacion"]
    cursor1 = baseDatos.cursor()
    sql = f"SELECT * FROM usuarios WHERE usuario='{usuario}'"
    cursor1.execute(sql)
    resultado = cursor1.fetchall()
    print(len(resultado))
    if len(resultado) == 1:
        return render_template("register.html",usuarios=usuario,celulares=celular, correos=email, contraseñas=contraseña,mensaje1="usuario ocupado")
    elif len(resultado) == 0:
        if contraseña != confirmacion:
            return render_template("register.html",usuarios=usuario,celulares=celular, correos=email, contraseñas=contraseña,mensaje2="contraseña distinta" )
        else:
            cursor2 = baseDatos.cursor()
            sql2 = f"INSERT INTO usuarios VALUES('{usuario}','{contraseña}','{celular}','{email}')"
            cursor2.execute(sql2)
            baseDatos.commit()
            return redirect("/login")

if __name__=="__main__":
    programa.run(host="0.0.0.0",debug="True",port="5080")