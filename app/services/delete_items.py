from app import app, db
from flask import render_template, request, session, redirect, url_for, jsonify
from app.models.db_function import EstTeklaData
from app.models.user import render_by_role

@app.route('/delete_item')
def delete_item():
    """Renderiza la interfaz para eliminar elementos."""
    return render_template('z_tools/delete_items.html')

@app.route('/procesar_busqueda_eliminar', methods=['POST'])
def procesar_busqueda_eliminar():
    """Procesa la búsqueda de elementos según el filtro aplicado."""
    search_filter = request.form.get('search_filter', '')

    search_results = EstTeklaData.query.filter(EstTeklaData.PIECEMARK.ilike(f"%{search_filter}%")).all()

    results = [
        {
            'id': item.ID,
            'piecemark': item.PIECEMARK,
            'esp': item.ESP,
            'linea': item.LINEA,
            'class': item.CLASS,
            'qty': item.QUANTITY,
            'weight': item.WEIGHT,
            'ratio': item.RATIO
        } for item in search_results
    ]
    return jsonify({'search_results': results})

@app.route('/eliminar_elemento', methods=['POST'])
def eliminar_elemento():
    """Elimina un elemento de la base de datos dado su ID."""
    if 'username' in session:
        item_id = request.form.get('id')

        elemento = EstTeklaData.query.filter_by(ID=item_id).first()

        if elemento:
            db.session.delete(elemento)
            db.session.commit()
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Elemento no encontrado"}), 404
    else:
        # Usa la función `render_by_role` para devolver la plantilla según el rol
        context = {}
        return render_by_role('index', context)
