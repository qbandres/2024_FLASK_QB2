from flask import url_for

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