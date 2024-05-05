from app import app
from app.services.sql_processor import Consultas_sql
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import render_by_role
from flask import request, session, redirect, url_for, flash,send_file, jsonify,render_template
from datetime import datetime


@app.route('/search_elements', methods=['GET', 'POST'])
def search_elements():
    # Inicializa la variable al comienzo de la función
    
    id_filter = esp_filter = linea_filter = class_filter = weight_condition = weight_value = None

    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        # Devuelve la página inicial para el formulario
        return render_template('search_elements.html', filtered_data=filtered_data)

    elif request.method == 'POST':
            try:
                # Recuperar los valores de los filtros del formulario
                id_filter = request.form.get('id_filter')
                esp_filter = request.form.get('esp_filter')
                linea_filter = request.form.get('linea_filter')
                class_filter = request.form.get('class_filter')
                weight_condition = request.form.get('weight_condition')
                weight_value = request.form.get('weight_value', type=float)

                # Crear un objeto de consulta y realizar el filtrado
                ConsultaSql = Consultas_sql()
                filtered_data = ConsultaSql.filter_sql(
                    None, id_filter, esp_filter, linea_filter, class_filter, weight_condition, weight_value
                )

            except SQLAlchemyError as e:
                return jsonify({'error': f"Ocurrió un error al procesar la búsqueda: {e}"}), 500
            except ValueError as e:
                return jsonify({'error': f"Error en el formato del ID: {e}"}), 400
            
            # Convierte los resultados en formato JSON para AJAX
            resultado = [
                {
                    'ID': item.ID,
                    'PIECEMARK': item.PIECEMARK,
                    'BARCODE': item.BARCODE,
                    'ESP': item.ESP,
                    'PROFILE': item.PROFILE,
                    'LINEA': item.LINEA,
                    'DESCRIPTION': item.DESCRIPTION,
                    'CLASS': item.CLASS,
                    'QUANTITY': item.QUANTITY,
                    'WEIGHT': item.WEIGHT,
                    'RATIO': item.RATIO,
                    'TRASLADO': str(item.TRASLADO),
                    'PRE_ENSAMBLE': str(item.PRE_ENSAMBLE),
                    'MONTAJE': str(item.MONTAJE),
                    'TORQUE': str(item.TORQUE),
                    'PUNCH': str(item.PUNCH)
                } for item in filtered_data
            ]

            return jsonify({'data': resultado})