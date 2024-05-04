from flask import render_template, request, session, redirect, url_for, flash
from app.models.user import Roles
from app.models.db_function import User
from app import app
from sqlalchemy.exc import SQLAlchemyError

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            # Solo intenta acceder a los valores cuando el formulario es enviado
            username = request.form['username']
            password = request.form['password']

            # Consulta a la base de datos
            user = User.query.filter_by(username=username).first()

            # Verifica que el usuario exista y que la contraseña sea correcta
            # Aquí se asume que la contraseña no está hasheada
            if user is not None and user.password_hash == password:
                session['username'] = username
                session['rol'] = user.rol  # Asegúrate de que 'rol' es un atributo de tu modelo de usuario

                print(Roles.redireccionar_segun_rol(user.rol))

                return redirect(Roles.redireccionar_segun_rol(user.rol))
            else:
                # Mostrar un mensaje de error en caso de credenciales incorrectas
                flash('Credenciales incorrectas', 'error')

        except SQLAlchemyError as e:
            # Maneja la excepción genérica de SQLAlchemy
            flash('Error de acceso a la base de datos', 'error')
            app.logger.error(f'Error de acceso a la base de datos: {e}')
            
        # Renderiza la plantilla de login si el inicio de sesión falla o si hay una excepción
        return render_template('z_tools/login.html')
    else:
        # Cuando es un método GET, simplemente renderiza la plantilla del formulario de inicio de sesión
        return render_template('z_tools/login.html')