from flask import Flask, render_template, request, session, redirect, url_for
from threading import Thread
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'OnETP_@///3835#?425=$425$#y425d33j_db425wfjsefes_2241skf425HhA4_323wkE5nfsfnNFlAsK.oN' # NO TOCAR EL TOKEN SIN ESTO NO ANDA NADA 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onetp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# esto ya no lo vamos a usar ya que es una bad basada en RAM (se borra al reiniciar/apagar)

# "Base de datos" simulada en memoria
usuarios_registrados = {}  # Usuarios
aerolineas_registradas = {}  # Aerolíneas
vuelos_registrados = {} #Vuelos
vehiculos_registrados = {} #Vehiculos
alquileres_registrados = {} #Alquileres


# https://onetp-1-2tic.onrender.com






# Tabla SQL solo para usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    gmail = db.Column(db.String(100))
    telefono = db.Column(db.String(20))


class Aereolinea(db.Model):
    __tablename__ = 'aereolinea'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(100), nullable=False)
    cantvuelos = db.Column(db.Integer, nullable=False)

class Vuelo(db.Model):
    __tablename__ = 'vuelo'
    id = db.Column(db.Integer, primary_key=True)
    aerolineas = db.Column(db.Integer, foreing_key=True)
    salida = db.Column(db.String(100), nullable=False)
    escalas = db.Column(db.String(500))
    destino = db.Column(db.String(100), nullable=False)
    asiento = db.Column(db.String(100), nullable=False)
    duracio = db.Column(db.DateTime, nullable=False)
    clase = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    metodopago = db.Column(db.String(100), nullable=False)

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    modelovehi = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    patente = db.Column(db.String(100), nullable=False)
    kilometro = db.Column(db.String(100), nullable=False)

class Alquiler(db.Model):
    __tablename__ = 'alquiler'
    id = db.Column(db.Integer, primary_key=True)
    vehiculo = db.Column(db.Integer, foreing_key=True)
    empresa = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    metodopago = db.Column(db.String(100), nullable=False)

class Paquetes(db.Model):
    __tablename__ = 'paquetes'
    id = db.Column(db.Integer, primary_key=True)
    vuelo = db.Column(db.Integer, foreing_key=True)
    alquiler = db.Column(db.Integer, foreing_key=True)
    locacion = db.Column(db.Integer, foreing_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    duracion = db.Column(db.Date, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    metodopago = db.Column(db.String(100), nullable=False)

class Alojamientos(db.Model):
    __tablename__ = 'alojamientos'
    id = db.Column(db.Integer, primary_key=True)
    estadia = db.Column(db.String(200), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    metodopago = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    usuario = session.get('usuario')
    aerolineas = Aereolinea.query.all()
    vuelos = Vuelo.query.all()
    vehiculos = Vehiculo.query.all()
    alquileres = Alquiler.query.all()
    alojamientos = Alojamientos.query.all()
    paquetes = Paquetes.query.all()
    return render_template("ONETP.html",
                           usuario=usuario,
                           aerolineas=aerolineas,
                           vuelos=vuelos,
                           vehiculos=vehiculos,
                           alquileres=alquileres,
                           alojamientos=alojamientos,
                           paquetes=paquetes
                          
                          )



@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        contraseña = request.form.get('contra', '').strip()
        rcontraseña = request.form.get('rcontra', '').strip()
        gmail = request.form.get('mail', '').strip()
        telefono = request.form.get('tele', '').strip()
        if usuario and contraseña and rcontraseña and gmail and telefono:
            if contraseña == rcontraseña:
                if Usuario.query.filter_by(nombre=usuario).first():# usemos esto en el login
                    return "⚠️ El usuario ya existe. Por favor elige otro.", 400
                nuevo_usuario = Usuario(nombre=usuario, contraseña=contraseña, gmail=gmail, telefono=telefono)#Teniendo en cuenta esto tambien
                db.session.add(nuevo_usuario)
                db.session.commit()
                session['usuario'] = usuario
                return redirect(url_for('index'))
            else:
                return "⚠️ Completa todos los campos.", 400
    return render_template("Registro.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario', '').strip()
        contraseña = request.form.get('contra', '').strip()
        if Usuario.query.filter_by(nombre=usuario, contraseña=contraseña).first():
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return "⚠️ Usuario o contraseña incorrectos.", 401
    return render_template("Login.html")


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/aerolinea', methods=['GET', 'POST'])
def aerolinea():
    usuario = session.get('usuario')
    if request.method == 'POST':
        nick_aero = request.form.get('aero_nick', '').strip()
        model = request.form.get('model', '').strip()
        matri = request.form.get('mat', '').strip()
        vuelo = request.form.get('cantv', '').strip()
        if nick_aero and model and matri and vuelo:
            nueva_aerolinea = Aereolinea(
                nombre=nick_aero,
                modelo=model,
                matricula=matri,
                cantvuelos=vuelo
            )
            db.session.add(nueva_aerolinea)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("Aerolinea.html", usuario=usuario)





@app.route('/vuelo', methods=['GET', 'POST'])
def vuelo():
    usuario = session.get('usuario')
    if request.method == 'POST':
        salida = request.form.get('sal', '').strip()
        escalas = request.form.get('esc', '').strip()
        destino = request.form.get('des', '').strip()
        asiento = request.form.get('asi', '').strip()
        duracion = request.form.get('dur', '').strip()
        clase = request.form.get('cla', '').strip()
        precio = request.form.get('pre', '').strip()
        metodop = request.form.get('met', '').strip()
        if salida and escalas and destino and asiento and duracion and clase and precio and metodop:
            nuevo_vuelo = Vuelo(
                salida=salida,
                escalas=escalas,
                destino=destino,
                asiento=asiento,
                duracio=duracion, 
                clase=clase,
                precio=precio,
                metodopago=metodop
            )
            db.session.add(nuevo_vuelo)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("Vuelo.html", usuario=usuario)



@app.route('/vehiculo', methods=['GET', 'POST'])
def vehiculo():
    usuario = session.get('usuario')
    if request.method == 'POST':
        marcas = request.form.get('marc', '').strip()
        modelov = request.form.get('modelv', '').strip()
        tipos = request.form.get('tip', '').strip()
        matriv = request.form.get('matv', '').strip()
        kilometros = request.form.get('kilo', '').strip()
        if marcas and modelov and tipos and matriv and kilometros:
            nuevo_vehiculo = Vehiculo(
                marca=marcas,
                modelovehi=modelov,
                tipo=tipos,
                patente=matriv,
                kilometro=kilometros
            )
            db.session.add(nuevo_vehiculo)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("Vehiculo.html", usuario=usuario)

@app.route('/alquiler', methods=['GET', 'POST'])
def alquiler():
    usuario = session.get('usuario')
    if request.method == 'POST':
        empresas = request.form.get('emp', '').strip()
        ciudades = request.form.get('ciu', '').strip()
        direccion = request.form.get('dire', '').strip()
        precios = request.form.get('prec', '').strip()
        metpago = request.form.get('mpago', '').strip()
        if empresas and ciudades and direccion and precios and metpago:
            nuevo_aquiler = Alquiler(
                empresa=empresas,
                ciudad=ciudades,
                direccion=tipos,
                precio=precios,
                metodopago=metpago
            )
            db.session.add(nuevo_aquiler)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("Alquiler.html", usuario=usuario)

@app.route('/paquetes', methods=['GET', 'POST'])
def paquetes():
    usuario = session.get('usuario')
    if request.method == 'POST':
        nombre = request.form.get('nom', '').strip()
        direcion = request.form.get('dur', '').strip()
        precio = request.form.get('prc', '').strip()
        pagomet = request.form.get('pagom', '').strip()
        if nombre and direcion and precio and pagomet:
            nuevo_paquete = Paquetes(
                nombre=nombre,
                direcion=duracion,
                precio=precio,
                metodopago=pagomet
            )
            db.session.add(nuevo_paquete)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("Paquete.html", usuario=usuario)

@app.route('/alojamiento', methods=['GET', 'POST'])
def alojamiento():
    usuario = session.get('usuario')
    if request.method == 'POST':
        estadia = request.form.get('est', '').strip()
        ciudad = request.form.get('ciu', '').strip()
        direcion = request.form.get('dur', '').strip()
        precio = request.form.get('prc', '').strip()
        pagomet = request.form.get('pagom', '').strip()
        if estadia and ciudad and direcion and precio and pagomet:
            nuevo_alojamiento = Alojamiento(
                estadia=estadia,
                ciudad=ciudad,
                direcion=direcion,
                precio=precio,
                metodopago=pagomet
            )
            db.session.add(nuevo_alojamiento)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("Alojamientos.html", usuario=usuario)


@app.route('/lista_usuarios')
def lista_usuarios():
    usuario = session.get('usuario')
    usuarios = Usuario.query.all()
    return render_template("Listado de usuarios.html", usuario=usuario, usuarios=usuarios)


def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    server = Thread(target=run)
    server.start()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
