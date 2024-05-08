from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Carga las variables de entorno del archivo .env
load_dotenv()

app = Flask(__name__)

# Configura la clave secreta y la URI de la base de datos a partir de las variables de entorno
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Aquí irían las demás configuraciones y la inicialización de otros componentes de tu aplicación Flask
# Imprimir valores de configuración
print("SECRET_KEY:", app.config['SECRET_KEY'])
print("SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])


#Importaciones de tus rutas, utilidades y modelos
from app.routes import login, index,main
from app.models import user,db_function
from app.services import sql_processor,excel_processor,graphic_processor,update_assembly,add_items,delete_items

# Aquí se agregarían más configuraciones o inicializaciones si fuesen necesarias