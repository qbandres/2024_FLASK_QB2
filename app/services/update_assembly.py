from app import app, db
from flask import render_template, request, session, redirect, url_for, jsonify
from app.models.db_function import EstTeklaData
from datetime import datetime

@app.route('/update_assembly')
def update_assembly():
    # Asegurarse de que el valor sea una cadena para filtrar
    datos_estaticos = EstTeklaData.query.filter_by(ID='1').first()

    search_filter = request.args.get('search_filter', '')

    return render_template('z_tools/update_assembly.html', datos_estaticos=datos_estaticos, search_filter=search_filter)

@app.route('/actualizar_montaje', methods=['POST'])
def actualizar_montaje():
    if 'username' in session:
        # Convertir ImmutableMultiDict a un diccionario mutable
        data = dict(request.form)

        # Reemplazar fechas vacías con None
        for field in ['traslado', 'pre_ensamble', 'montaje', 'torque', 'punch']:
            if not data.get(field):
                data[field] = None

        # Filtrar el elemento por ID
        elemento = EstTeklaData.query.filter_by(ID=data['id']).first()

        if elemento:
            # Actualizar valores del modelo
            elemento.TRASLADO = data['traslado']
            elemento.PRE_ENSAMBLE = data['pre_ensamble']
            elemento.MONTAJE = data['montaje']
            elemento.TORQUE = data['torque']
            elemento.PUNCH = data['punch']

            # Confirmar los cambios en la base de datos
            db.session.commit()
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Elemento no encontrado"}), 404
    else:
        return redirect(url_for('index'))

@app.route('/procesar_busqueda_actualizar', methods=['POST'])
def handle_procesar_busqueda_actualizar():
    search_filter = request.form.get('search_filter', '')
    

    search_results = EstTeklaData.query.filter(EstTeklaData.PIECEMARK.ilike(f"%{search_filter}%")).all()
    print('imprimeindooooooo',search_results)

    results = [
        {
            'id': item.ID,
            'piecemark': item.PIECEMARK,
            'esp': item.ESP,
            'linea': item.LINEA,
            'class': item.CLASS,
            'qty': item.QUANTITY,
            'weight': item.WEIGHT,
            'ratio': item.RATIO,
            'traslado': item.TRASLADO.isoformat() if item.TRASLADO else '',
            'pre_ensamble': item.PRE_ENSAMBLE.isoformat() if item.PRE_ENSAMBLE else '',
            'montaje': item.MONTAJE.isoformat() if item.MONTAJE else '',
            'torque': item.TORQUE.isoformat() if item.TORQUE else '',
            'punch': item.PUNCH.isoformat() if item.PUNCH else ''
        } for item in search_results
    ]

    print("Resultados devueltos:", results)
    return jsonify({'search_results': results})

