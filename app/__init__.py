from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import boto3
import os

# Función para obtener parámetros de AWS Systems Manager Parameter Store
def get_ssm_parameter(name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response['Parameter']['Value']

# Inicializa tu aplicación Flask
app = Flask(__name__)

# Intenta encontrar el archivo .env
if find_dotenv():
    # Carga las variables desde el archivo .env
    load_dotenv()
    secret_key = os.getenv('SECRET_KEY')
    sqlalchemy_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
else:
    # Si no se encuentra el archivo .env, usa Parameter Store
    secret_key = get_ssm_parameter('/myproject/prod/SECRET_KEY')
    sqlalchemy_uri = get_ssm_parameter('/myproject/prod/SQLALCHEMY_DATABASE_URI')

# Configura la aplicación con los valores obtenidos
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa SQLAlchemy
db = SQLAlchemy(app)

# Importa las rutas, modelos y servicios de tu aplicación
from app.routes import login, index, main
from app.models import user, db_function
from app.services import sql_processor, excel_processor, graphic_processor, update_assembly, add_items, delete_items
