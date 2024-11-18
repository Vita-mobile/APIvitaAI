import firebase_admin
from firebase_admin import credentials
import os
import json

# Leer las credenciales de Firebase desde una variable de entorno
firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')

# Verificar que la variable de entorno esté definida
if not firebase_credentials:
    raise ValueError("Enviroment variable FIREBASE_CREDENTIALS is not set.")

# Cargar las credenciales en formato JSON
credentials_json = json.loads(firebase_credentials)

print("Despues del json:", credentials_json)

# Inicializar la aplicación de Firebase
cred = credentials.Certificate(credentials_json)    
firebase_admin.initialize_app(cred)

# Importar firestore si es necesario para la base de datos
from firebase_admin import firestore
db = firestore.client()

# Función para obtener la base de datos Firestore
def get_db():
    return db
