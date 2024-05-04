import pandas as pd
from flask import send_file
from io import BytesIO


class DataExcel:
    def __init__(self):
        pass
    def convert_to_df(self, all_records, params=None):
        # Asegúrate de que tienes todos los campos que necesitas en el dataframe
        data = [{
            'ID': record.ID,
            'PIECEMARK': record.PIECEMARK,
            'BARCODE': record.BARCODE,
            'ESP': record.ESP,
            'PROFILE': record.PROFILE,
            'LINEA': record.LINEA,
            'DESCRIPTION': record.DESCRIPTION,
            'CLASS': record.CLASS,
            'QUANTITY': record.QUANTITY,
            'WEIGHT': record.WEIGHT,
            'RATIO': record.RATIO,
            'TRASLADO': record.TRASLADO,
            'PRE_ENSAMBLE': record.PRE_ENSAMBLE,
            'MONTAJE': record.MONTAJE,
            'TORQUE': record.TORQUE,
            'PUNCH': record.PUNCH
        } for record in all_records]

        # Convertir a DataFrame
        df = pd.DataFrame(data)
        return df
    
    def descargar_excel(self, df):
        # Convertir el DataFrame a Excel usando un buffer en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)  # Importante: mueve el cursor al inicio del stream
        return output
    
    def df_xy(self,df, factor, name_x, name_y, name_y1=0, name_y2=0, name_y3=0, name_y4=0, name_y5=0):
        # Lista para almacenar los nombres de las columnas 'y' que se incluirán
        y_columns = [name for name in [name_y, name_y1, name_y2, name_y3, name_y4, name_y5] if name != 0]

        # Seleccionar las columnas 'x' y las columnas 'y' especificadas
        df = df[[name_x] + y_columns].copy()

        df.columns = ['x'] + ['y' + str(i) for i in range(len(y_columns))]


        # Reemplazar '' con NaN y eliminar filas con NaN
        df.replace('', pd.NA, inplace=True)
        df = df.dropna()

        # Dividir las columnas 'y' por el factor
        for col in df.columns[1:]:
            df[col] = df[col] / factor

        # Sumar las columnas 'y' y resetear el índice
        df_sum = df.groupby('x').sum().reset_index()

        # Copiar df_sum para crear df_acum
        df_acum = df_sum.copy()

        # Calcular la suma acumulativa para cada columna 'y' por separado
        for col in df_acum.columns[1:]:  # Ignora la columna 'x'
            df_acum[col] = df_acum[col].cumsum()

        # df_acum ahora contiene la misma estructura de columnas que df_sum pero con valores acumulativos
        return df_sum, df_acum
    
    #Este metodo recibe un dataframe y el numero de columnas solo de y para extraer los maximos y minimos
    def max_min(self, data, num_y_columns=1):
            data['x'] = pd.to_datetime(data['x'])
            x_start = pd.to_datetime(data['x'].min())  # Fecha inicial
            x_end = pd.to_datetime(data['x'].max())    # Fecha final

            # Calcular la diferencia en días
            date_range = x_end - x_start

            # Calcular 5% de ese rango
            ten_percent = date_range * 0.05

            # Extender el rango en un 10%
            x_start = x_start - ten_percent
            x_end = x_end + ten_percent

            y_start = 0
            y_end = float('-inf')

            for i in range(num_y_columns):
                y_column_name = f'y{i}'  # Cambiado para empezar desde 'y0'
                y_end = max(y_end, data[y_column_name].max())
     
            y_end = float(y_end) * 1.1 # Extender el límite superior de y en un 10%

            return x_start, x_end, y_start, y_end
        



    
    # def regular_df(self, query, params=None):
    #     """
    #     Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de Pandas.
        
    #     Args:
    #     query (str): La consulta SQL a ejecutar.
    #     params (tuple, optional): Los parámetros a usar en la consulta SQL. Por defecto es None.

    #     Returns:
    #     DataFrame: Un DataFrame de Pandas con los resultados de la consulta SQL.
    #     """

    #     # Abre una nueva conexión y crea un nuevo cursor
    #     cursor = db_connection.cursor()

    #     # Ejecuta la consulta SQL, utilizando parámetros para prevenir inyección SQL
    #     cursor.execute(query, params or ())

    #     # Recupera todos los datos devueltos por la consulta
    #     table_data = cursor.fetchall()

    #     # Obtiene dinámicamente los nombres de las columnas de los metadatos de la consulta
    #     column_names = [description[0] for description in cursor.description]

    #     # Cierra el cursor
    #     cursor.close()

    #     # Crea y devuelve un DataFrame de Pandas con los datos y nombres de columna
    #     df = pd.DataFrame(table_data, columns=column_names)
    #     return df
    
    # def procesar_busqueda_actualizar(self):
    #     search_filter = request.form.get('search_filter')
        
    #     # Aquí asumimos que deseas buscar coincidencias en la columna 'piecemark'
    #     cursor = db_connection.cursor()
    #     query = "SELECT * FROM est_tekladata WHERE piecemark ILIKE %s"
    #     cursor.execute(query, ('%' + search_filter + '%',))
    #     resultados = cursor.fetchall()
    #     cursor.close()

    #     # Convertir los resultados a una lista de diccionarios o similar, según sea necesario
    #     search_results = [{"id": res[0], "piecemark": res[1],"esp": res[2],"linea": res[3],"class": res[4],"qty": res[5],"weight": res[6],"ratio": res[7],"zona": res[8],"traslado": res[9],"pre_ensamble": res[10],"montaje": res[11],"torque": res[12],"punch": res[13]} for res in resultados]
        
    #     return jsonify({"search_results": search_results})
    
    # def regular_list(self, query, params=None):
    #     """
    #     Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de Pandas.
        
    #     Args:
    #     query (str): La consulta SQL a ejecutar.
    #     params (tuple, optional): Los parámetros a usar en la consulta SQL. Por defecto es None.

    #     Returns:
    #     DataFrame: Un DataFrame de Pandas con los resultados de la consulta SQL.
    #     """

    #     # Abre una nueva conexión y crea un nuevo cursor
    #     cursor = db_connection.cursor()

    #     # Ejecuta la consulta SQL, utilizando parámetros para prevenir inyección SQL
    #     cursor.execute(query, params or ())

    #     # Recupera todos los datos devueltos por la consulta
    #     table_data = cursor.fetchall()

    #     # Obtiene dinámicamente los nombres de las columnas de los metadatos de la consulta
    #     column_names = [description[0] for description in cursor.description]

    #     # Cierra el cursor
    #     cursor.close()

    #     # Crea una lista de diccionarios, donde cada diccionario representa una fila
    #     result_list = [row[0] for row in table_data]
    #     return result_list
    
    # def procesar_busqueda_dash(self,query,search_filter1=None, search_filter2=None, search_filter3=None, search_filter4=None):
    #     # Inicializa la lista de parámetros.
    #     print(search_filter1)
    #     print(search_filter2)
    #     print(search_filter3)
    #     print(search_filter4)

    #     conditions = []
    #     params = []


    #     search_filter1 = tuple(item.strip() for item in ast.literal_eval(search_filter1))
    #     search_filter2 = tuple(item.strip() for item in ast.literal_eval(search_filter2))
    #     search_filter3 = tuple(item.strip() for item in ast.literal_eval(search_filter3))
    #     search_filter4 = tuple(item.strip() for item in ast.literal_eval(search_filter4))

    #     if search_filter1:
    #         conditions.append(f"esp IN ({', '.join(['%s'] * len(search_filter1))})")
    #         params.extend(search_filter1)
    #     if search_filter2:
    #         conditions.append(f"linea IN ({', '.join(['%s'] * len(search_filter2))})")
    #         params.extend(search_filter2)
    #     if search_filter3:
    #         conditions.append(f"class IN ({', '.join(['%s'] * len(search_filter3))})")
    #         params.extend(search_filter3)
    #     if search_filter4:
    #         conditions.append(f"zona IN ({', '.join(['%s'] * len(search_filter4))})")
    #         params.extend(search_filter4)

    #     query = "SELECT * FROM est_tekladata"

    #     # Añadir las condiciones a la consulta si existen
    #     if conditions:
    #         query += " WHERE " + " AND ".join(conditions) + ";"
    #     else:
    #         # Si no se proporcionan filtros, utilizar una consulta predeterminada
    #         query += " WHERE qty > 0;"  # Reemplazar con tu condición predeterminada

    #     # Asumiendo que params solo contiene cadenas o números
    #     # (tener cuidado de la inyección de SQL si se incluyen entradas directamente de los usuarios)
    #     query_debug = query
    #     for p in params:
    #         # Asegurar que los marcadores de posición se reemplacen con cadenas debidamente entrecomilladas
    #         query_debug = query_debug.replace("%s", repr(str(p)), 1)  # reemplazar cada %s con su valor en params

    #     print("Consulta de depuración:", query_debug)
    #     print(query)



    #     print(query)
    #     print(query)
  
    #     # Conecta a la base de datos y ejecuta la consulta.
    #     cursor = db_connection.cursor()
    #     cursor.execute(query, tuple(params))
    #     resultados = cursor.fetchall()
    #     cursor.close()

    #     # Si no hay resultados, no habrá descripción y esto causará un error.
    #     if not resultados:
    #         return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay resultados.

    #     column_names = [description[0] for description in cursor.description]

    #     df = pd.DataFrame(resultados, columns=column_names)

    #     print("el dataframes :",df)

    #     # Convertir los resultados a una lista de diccionarios.
    #     # search_results = [{"id": res[0], "piecemark": res[1], "esp": res[2],"linea": res[3], "class": res[4], "qty": res[5],"weight": res[6], "ratio": res[7], "zona": res[8],"traslado": res[9], "pre_ensamble": res[10], "montaje": res[11],"torque": res[12], "punch": res[13]} for res in resultados]

    #     # print(search_results)

    #     return df
    
    # def descargar_excel(self, query, file_name="datos_exportados.xlsx"):
    #     # Ejecuta la consulta y obtiene los resultados en un DataFrame
    #     df = self.regular_df(query)

    #     # Convertir el DataFrame a Excel usando un buffer en memoria
    #     output = BytesIO()
    #     with pd.ExcelWriter(output, engine='openpyxl') as writer:
    #         df.to_excel(writer, index=False)