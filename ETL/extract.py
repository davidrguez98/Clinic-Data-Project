from datetime import datetime
from database.connection import DentalClinicDatabase

class DataExtractor:

    def __init__(self, database_name: str, test_date: str = None):
        self.clinic = DentalClinicDatabase(database=database_name)

        # Opción por si se le pasa una fecha concreta
        if test_date:
            self.today = test_date
        else:
            self.today = datetime.today().strftime('%Y-%m-%d')

    # Ejecuta una query y devuelve los resultados
    def _execute_query(self, query: str, params: tuple = None):
        connection = None

        try:

            connection = self.clinic.get_connection()

            if connection is None:
                raise Exception('Error during the connection to the database')
            
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            return result
        except Exception as error:
            print(f"Error during request {error}")
            return None
        finally:
            if connection:
                connection.close()

    # Obtiene y devuelve la cantidad de citas del día
    def get_appointments_count(self):
        query = "SELECT COUNT(*) FROM appointments WHERE DATE(date_time)=%s"
        result = self._execute_query(query, (self.today,))

        if result:
            return result[0][0]
        return 0
    
    # Obtiene y devuelve información de los trabajadores sin procesar
    def get_workers_raw_data(self):
        query = """
            SELECT b.name, DATE_FORMAT(a.date_time, '%H:%i'), a.reason 
            FROM appointments AS a 
            JOIN workers AS b ON a.id_worker = b.id_worker 
            WHERE DATE(a.date_time)=%s 
            ORDER BY b.name, a.date_time
        """
        result = self._execute_query(query, (self.today,))

        if result:
            return result
        return []
    
    # Obtiene la facturación del día
    def get_billing_total(self):
        query = """
            SELECT SUM(total) 
            FROM appointments AS a 
            JOIN receipts AS b ON a.id_appointment = b.id_appointment 
            WHERE DATE(a.date_time)=%s
        """

        result = self._execute_query(query, (self.today,))

        if result:
            result = int(result[0][0])
            return result
        return 0