import os
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()

# Configuración de la base de datos, dejando como primera opción el nombre de la variable de entorno y en segundo la conexión en local
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}