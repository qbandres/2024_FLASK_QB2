from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def requiere_rol(rol_requerido):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                flash('Por favor, inicia sesión para continuar.', 'warning')
                return redirect(url_for('login'))
            elif 'rol' not in session or session['rol'] != rol_requerido:
                print('tercer impresion')
                print(rol_requerido)
                print(session.get('rol'))
                flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


