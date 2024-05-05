from flask import render_template, url_for,render_template, flash, session,redirect

class Roles:
    def __init__(self):
        pass

    def redireccionar_segun_rol(rol):
        rutas_rol = {
            'management': 'index_management',
            'site': 'index_site',
            'ot': 'index_ot',
            'admin': 'index_admin'
                    }
        return url_for(rutas_rol.get(rol))
    
def render_by_role(template_name, context):
    """Función que redirige según el rol del usuario."""
    role_templates = {
        'management': 'management/index.html',
        'site': 'site/index.html',
        'ot': 'ot/index.html',
        'admin': 'admin/index.html'
    }

    rol = session.get('rol')
    template = role_templates.get(rol)

    if template:
        return render_template(template, **context)
    else:
        flash('Rol no reconocido o no tienes permisos suficientes.', 'error')
        return redirect(url_for('login'))
