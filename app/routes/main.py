from app import app
from app.services.sql_processor import Consultas_sql
from app.services.excel_processor import DataExcel
from app.services.graphic_processor import BokehGraph
from flask import request, session, redirect, url_for, flash,send_file, jsonify,render_template
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import render_by_role


@app.route('/download_excel')
def download_excel():
    consulta = Consultas_sql()
    excel_export = DataExcel()

    table = consulta.all_sql()
    df = excel_export.convert_to_df(table)
    output = excel_export.descargar_excel(df)
    return send_file(output, download_name="Nuevo Archivo.xlsx", as_attachment=True)

def generate_graph_data():
    consulta = Consultas_sql()
    excel_export = DataExcel()
    table = consulta.all_sql()
    df = excel_export.convert_to_df(table)

    df1, df1_acum = excel_export.df_xy(df, 1000, 'MONTAJE', 'WEIGHT')

    
    # Creación de gráficos con Bokeh
    bokehGraph = BokehGraph()
    script1, div1 = bokehGraph.scatter(df1,'Date', 'Ton', 'Montaje Diario Variación Scatter')
    script2, div2 = bokehGraph.linear(df1_acum,'Date', 'Ton', 'Montaje Acumulado Variación Linear')
    # script3, div3 = bokehGraph.bar_chartMes(df2,'Date', 'Ton', 'Montaje Mensual Variación bar_chart')
    return script1, div1,script2, div2 

    
@app.route('/redirigir_principal')
def redirigir_principal():
    # Crear un contexto vacío o personalizarlo si se requiere
    context = {}
    return render_by_role('index.html', context)