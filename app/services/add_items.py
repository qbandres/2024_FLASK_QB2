from flask import render_template, request, redirect, url_for, flash
from app import app, db  # Importa el objeto `db` de SQLAlchemy
from app.models.db_function import EstTeklaData  # Importa el modelo correspondiente
from app.models.user import render_by_role

@app.route('/anadir_elemento', methods=['GET', 'POST'])
def anadir_elemento():
    if request.method == 'POST':
        # Obtener datos del formulario como listas
        IDs = request.form.getlist('ID[]')
        PIECEMARKs = request.form.getlist('PIECEMARK[]')
        ESPs = request.form.getlist('ESP[]')
        LINEAs = request.form.getlist('LINEA[]')
        CLASSes = request.form.getlist('CLASS[]')
        QTYs = request.form.getlist('QTY[]')
        WEIGHTs = request.form.getlist('WEIGHT[]')
        RATIOs = request.form.getlist('RATIO[]')
        ZONAs = request.form.getlist('ZONA[]')

        # Intentar insertar cada nuevo elemento en la base de datos
        try:
            for i in range(len(IDs)):
                nuevo_elemento = EstTeklaData(
                    ID=IDs[i],
                    PIECEMARK=PIECEMARKs[i],
                    ESP=ESPs[i],
                    LINEA=LINEAs[i],
                    CLASS=CLASSes[i],
                    QUANTITY=QTYs[i],
                    WEIGHT=WEIGHTs[i],
                    RATIO=RATIOs[i],
                    ZONA=ZONAs[i],
                    TRASLADO=None,
                    PRE_ENSAMBLE=None,
                    MONTAJE=None,
                    TORQUE=None,
                    PUNCH=None
                )
                db.session.add(nuevo_elemento)
            db.session.commit()  # Guardar los cambios en la base de datos
            flash('Elementos añadidos con éxito.', 'success')
        except Exception as e:
            print("Error:", e)
            db.session.rollback()  # Revertir la transacción si ocurre un error
            flash('Error al añadir los elementos.', 'error')

        return redirect(url_for('main'))

    # Si el método es GET, renderiza el formulario de añadir elemento
    return render_template('z_tools/add_items.html')
