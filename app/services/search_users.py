from app import app, db
from flask import request, session, redirect, url_for, jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError
from app.models.db_function import User

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
