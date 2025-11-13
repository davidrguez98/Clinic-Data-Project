import mysql.connector
from config.database import DATABASE_CONFIG

# Clase simulando una clínica dental conectada mediante BBDD SQL
class DentalClinicDatabase:

    # Constructor para recibir el nombre de la BBDD
    def __init__(self, database):
        #Copia de la configuración de la BBDD para no modificar el código de ejemplo
        self.config = DATABASE_CONFIG.copy()
        self.config["database"] = database

    #Función para conectarnos a la base de datos
    def get_connection(self):

        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except mysql.connector.Error as error:
            print(f"Error connecting to the database {error}")
            return None