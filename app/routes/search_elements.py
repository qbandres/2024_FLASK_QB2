# from flask import render_template, request, session, redirect, url_for, flash
# from app import app
# from sqlalchemy.exc import SQLAlchemyError
# from ..services.sql_processor import Consultas_sql

# # En search_elements.py
# filtered_data = None  # Define la variable a nivel de módulo
# all_table = None  # Define la variable a nivel de módulo

# @app.route('/search_elements', methods=['GET', 'POST'])
# def search_elements():
#     global filtered_data, all_table

#     # Inicializa la variable al comienzo de la función
    
#     id_filter = esp_filter = linea_filter = class_filter = weight_condition = weight_value = None

#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         try:
#             # Recupere los valores de los filtros del formulario
#             id_filter = request.form.get('id_filter')
#             esp_filter = request.form.get('esp_filter')
#             linea_filter = request.form.get('linea_filter')
#             class_filter = request.form.get('class_filter')
#             weight_condition = request.form.get('weight_condition')
#             weight_value = request.form.get('weight_value', type=float)  # Asegúrese de convertir a float

#             ConsultaSql = Consultas_sql()
#             #Llamar al método filter_sql con los parámetros adecuados
#             filtered_data = ConsultaSql.filter_sql(None, id_filter, esp_filter, linea_filter, class_filter, weight_condition, weight_value)

#         except SQLAlchemyError as e:
#             flash(f"Ocurrió un error al procesar la búsqueda: {e}", 'error')
#             app.logger.error(f"Error en /search_elements: {e}")
#         except ValueError as e:
#             flash(f"Error en el formato del ID: {e}", 'error')

#     return render_template('management/index.html', 
#                        filtered_data=filtered_data)
