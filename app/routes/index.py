from flask import session, render_template
from app import app
from app.utilities.decorators import requiere_rol
from app.routes.main import generate_graph_data
from app.services.search_elements import search_elements


search_main_table=None


@app.route('/index_management')
@requiere_rol('management')
def index_management():
    script1, div1, script2, div2 = generate_graph_data()
    # No necesitas verificar 'username' en session aquí, el decorador ya lo hizo.
    return render_template("management/index.html", script1=script1, div1=div1,script2=script2, div2=div2)

@app.route('/index_site')
@requiere_rol('site')
def index_site():
    # No necesitas verificar 'username' en session aquí, el decorador ya lo hizo.
    return render_template('site/index.html')

@app.route('/index_ot')
@requiere_rol('ot')
def index_ot():
    # No necesitas verificar 'username' en session aquí, el decorador ya lo hizo.
    return render_template('ot/index.html')
    # return render_template('index_ot.html')

@app.route('/index_admin')
@requiere_rol('admin')
def index_admin():
    # No necesitas verificar 'username' en session aquí, el decorador ya lo hizo.
    return render_template('admin/index.html')
    # return render_template('index_administrador.html')
