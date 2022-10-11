# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session
import os
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database_boom.db")



app = Flask(__name__)

app.secret_key = '54SF4GHAFHGAS4'

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/login_interfaz',methods=['POST'])
def login():
    Cedula = request.form.get("Cedula")
    password = request.form.get("Password")
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()    
    sql = "SELECT  Password, nombre  FROM registro WHERE Cedula=?"    
    cursor_db.execute(sql, (Cedula,))
    fila = cursor_db.fetchone()
    session["Cedula"] = Cedula   
    if fila is not None:
       if password==fila[0]:
        return redirect(url_for('menus_interfaz'))
       return "cedula o contraseña incorrecta."
    return "usurio no existe"

@app.route('/login_interfaz')
def login_interfaz():
    return render_template('login.html')

@app.route('/comprar/<idproducto>',  methods=['GET'])
def comprar_f(idproducto):
    if "Cedula" in session:
        Cedula =  session["Cedula"]
        return "Señor {} Ud ha comprado el articulo de id {}".format(Cedula, idproducto)
    return "Por favor inicie sesión"

@app.route('/cerrarsesion',  methods=['GET'])
def cerrar_sesion():
    if "Cedula" in session:
        session.pop("Cedula")
        return "sesión cerrada"
    return "Por favor inicie sesión"




@app.route('/login_admi_interfaz',methods=['POST'])
def login_admin():
    correo = request.form.get("correo")
    contraseña = request.form.get("contraseña")
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()    
    sql = "SELECT  contraseña  FROM administrador WHERE correo=?"      
    cursor_db.execute(sql, (correo,))
    fila = cursor_db.fetchone()    
    if fila is not None:
       if contraseña==fila[0]:
        return redirect(url_for('menu_insert_interfaz'))
       return "cedula o contraseña incorrecta."
    return "usurio no existe"
    

@app.route('/login_admi_interfaz')
def login_admi_interfaz():
    return render_template('login_admi.html')
    



@app.route('/registro',methods=['POST'])
def registro():
    correo = request.form.get("correo")
    nombre = request.form.get("nombre")
    numero_mesa= request.form.get("numero_mesa")
    Cedula = request.form.get("Cedula")
    Password= request.form.get("Password")
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()
    sql = "INSERT INTO registro(correo, nombre,numero_mesa, Cedula, Password) VALUES(?, ?, ?, ?, ?)"
    cursor_db.execute(sql, (correo,nombre,numero_mesa, Cedula , Password,))
    con_bd.commit()
    cursor_db.close()
    proveedor_correo = 'smtp.gmail.com: 587'
    remitente = 'Losrebeldes.0203@gmail.com'
    password = 'losrebeldes123'
    servidor = smtplib.SMTP(proveedor_correo)
    servidor.starttls()
    servidor.ehlo()
    servidor.login(remitente, password)
    mensaje = "<h1>Bienvenido a Mega Boom</h1>"
    msg = MIMEMultipart()
    msg.attach(MIMEText(mensaje, 'html'))
    msg['From'] = remitente
    msg['To'] = correo
    msg['Subject'] = 'Registro Exitoso'
    servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
    return redirect(url_for('login_interfaz'))
    

@app.route('/registro_interfaz')
def registro_interfaz():
    return render_template('registro.html')




@app.route('/menus')
def menus():
    nombre = request.form.get("nombre")
    return redirect(url_for('menu_shots_interfaz', 'menu_snacks_interfaz'), usuario = nombre)

@app.route('/menus_interfaz')
def menus_interfaz():
    return render_template('menus.html')




@app.route('/menu_shots', methods=['POST'])
def select_shots():
    ID_shots = request.form.get("ID_shots")
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()
    sql = "SELECT Precio FROM  shots WHERE ID_shots=?"
    cursor_db.execute(sql, (ID_shots,))
    fila = cursor_db.fetchone()
    if len(fila) > 0:
     
     return redirect(url_for('aviso_shot_interfaz', ID_shots=ID_shots))

@app.route('/menu_shots_interfaz')
def select_shots_interfaz():
    ID_shots = request.form.get("ID_shots")
    return render_template('menu_shots.html', ID_shots=ID_shots)



@app.route('/menu_snacks', methods=['POST'])
def select_snacks():
    ID_snakcks = request.form.get("ID_snakcks")
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()
    sql = "SELECT Precio FROM  snacks WHERE ID_snakcks=?"
    cursor_db.execute(sql, (ID_snakcks,))
    fila = cursor_db.fetchone()
    if len(fila) > 0:
    
     return redirect(url_for('aviso_snack_interfaz', ID_snakcks=ID_snakcks))
    
    
    

@app.route('/menu_snacks_interfaz')
def menu_snacks():
    ID_snakcks = request.form.get("ID_snakcks")
    return render_template('menu_snacks.html', ID_snakcks=ID_snakcks)




@app.route('/menu_insert')
def menu_insert():
    return redirect(url_for('menu_insert_shots_interfaz', 'menu_insert_snacks_interfaz'))

@app.route('/menu_insert_interfaz')
def menu_insert_interfaz():
    return render_template('menu_insert.html')
    

@app.route('/insert_shots',methods=['POST'])
def insert_shots():
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()
    sql = "INSERT INTO shots(nombre_shots, Precio) VALUES(?,?)"
    shots = request.form.get("nombre_shots")
    precio = request.form.get("Precio")
    cursor_db.execute(sql, (shots, precio))
    con_bd.commit()
    cursor_db.close()
    #return redirect(url_for('Insert_shot_interfaz'))
    return render_template('insert_shot.html')

@app.route('/Insert_shot_interfaz')
def insert_shot():
    return render_template('insert_shot.html')




@app.route('/insert_snaks',methods=['POST'])
def insert_snaks():
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()
    sql = "INSERT INTO snacks(nombre_snacks, Precio) VALUES(?,?)"
    snack = request.form.get("nombre_snacks")
    precio = request.form.get("Precio")
    cursor_db.execute(sql, (snack, precio))
    con_bd.commit()
    cursor_db.close()
    return render_template('insert_snack.html')

@app.route('/Insert_snacks_interfaz')
def insert_snack():
    return render_template('insert_snack.html')



@app.route('/aviso_shot', methods=['POST'])
def aviso_shots():
    ID_shots = request.form.get("ID_shots")
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()
    sql = "SELECT Precio FROM  shots WHERE ID_shots=?"
    cursor_db.execute(sql, (ID_shots,))
    fila = cursor_db.fetchone()
    if len(fila) > 0:
     
     return redirect(url_for('aviso_shot_interfaz', ID_shots=ID_shots))

@app.route('/aviso_shot_interfaz')
def aviso_shot_interfaz():
    ID_shots = request.form.get("ID_shots")
    return render_template('aviso_shots.html', ID_shots=ID_shots)



@app.route('/aviso_snack', methods=['POST'])
def aviso_snacks():
    ID_snakcks = request.form.get("ID_snakcks")
    con_bd = sqlite3.connect('database_boom.db')
    cursor_db = con_bd.cursor()
    sql = "SELECT Precio FROM  snacks WHERE ID_snakcks=?"
    cursor_db.execute(sql, (ID_snakcks,))
    fila = cursor_db.fetchone()
    if len(fila) > 0:
    
     return redirect(url_for('aviso_snack_interfaz', ID_snakcks=ID_snakcks))

@app.route('/aviso_snack_interfaz')
def aviso_snack_interfaz():
    return render_template('aviso_snacks.html')    

app.run(debug = True, port=5000)
