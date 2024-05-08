from app import app, db
from flask import request, session, redirect, url_for, jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError
from app.models.db_function import User

# Ruta para buscar usuarios
@app.route('/search_users', methods=['GET', 'POST'])
def search_users():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('search_users.html')
    elif request.method == 'POST':
        try:
            username_filter = request.form.get('username_filter')
            email_filter = request.form.get('email_filter')
            role_filter = request.form.get('role_filter')

            query = db.session.query(User)

            if username_filter:
                query = query.filter(User.username.ilike(f"%{username_filter}%"))
            if email_filter:
                query = query.filter(User.email.ilike(f"%{email_filter}%"))
            if role_filter:
                query = query.filter(User.rol.ilike(f"%{role_filter}%"))

            filtered_users = query.all()

            resultado = [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'rol': user.rol,
                    'password': '****'  # Ocultar con asteriscos por defecto
                } for user in filtered_users
            ]

            return jsonify({'data': resultado})

        except SQLAlchemyError as e:
            return jsonify({'error': f"Ocurrió un error al procesar la búsqueda: {e}"}), 500

# Ruta para obtener la contraseña
@app.route('/get_password', methods=['POST'])
def get_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = request.form.get('id')

    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            return jsonify({'password': user.password_hash})
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except SQLAlchemyError as e:
        return jsonify({'error': f"Error al recuperar contraseña: {e}"}), 500

# Ruta para eliminar usuario
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = request.form.get('id')

    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except SQLAlchemyError as e:
        return jsonify({'error': f"Error al eliminar usuario: {e}"}), 500

# Ruta para actualizar usuario
@app.route('/update_user', methods=['POST'])
def update_user():
    if 'username' not in session:
        return jsonify({'error': 'No hay sesión activa. Inicia sesión nuevamente.'}), 401

    user_id = request.form.get('id')
    username = request.form.get('username')
    email = request.form.get('email')
    rol = request.form.get('rol')
    new_password = request.form.get('password')

    try:
        user = db.session.query(User).filter_by(id=user_id).first()
        if user:
            user.username = username
            user.email = email
            user.rol = rol

            # Solo actualizar la contraseña si se proporciona una nueva
            if new_password:
                user.password_hash = new_password

            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404

    except SQLAlchemyError as e:
        return jsonify({'error': f"Error al actualizar usuario: {e}"}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    if 'username' not in session:
        return jsonify({'error': 'No hay sesión activa. Inicia sesión nuevamente.'}), 401

    # Obtener los datos del formulario
    username = request.form.get('username')
    email = request.form.get('email')
    rol = request.form.get('rol')
    password = request.form.get('password')

    # Validar que todos los campos necesarios estén presentes
    if not all([username, email, rol, password]):
        return jsonify({'error': 'Todos los campos son obligatorios.'}), 400

    try:
        # Crear un nuevo objeto de usuario
        nuevo_usuario = User(username=username, email=email, rol=rol, password_hash=password)

        # Añadir el nuevo usuario a la sesión
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({'success': True})

    except SQLAlchemyError as e:
        return jsonify({'error': f"Ocurrió un error al agregar el usuario: {e}"}), 500

