from datetime import datetime
import json
import os

from database.connection import DentalClinicDatabase

# Nombre de la base de datos a la que nos vamos a conectar
clinic = DentalClinicDatabase(database="dental_clinic")

# Selección del día de hoy
today = datetime.today().strftime('%Y-%m-%d')

# Creado solo para pruebas de peticiones
today='2025-11-15'

# Petición a la BBDD
def request_bbdd(query: str, params: tuple = None):

    try:
        connection = clinic.get_connection()
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


# Cantidad citas del día
def get_appointments_today():
    query = "SELECT COUNT(*) FROM appointments WHERE DATE(date_time)=%s"
    appointments_quantity = request_bbdd(query, (today,))

    return appointments_quantity[0][0]

# Personal de la empresa que ha trabajado
def get_workers_today():
    query = "SELECT b.name, DATE_FORMAT(a.date_time, '%h:%i'), a.reason FROM appointments AS a JOIN workers AS b ON a.id_worker = b.id_worker WHERE DATE(a.date_time)=%s ORDER BY b.name, a.date_time"
    workers_today = request_bbdd(query, (today,))

    return workers_today

# Formatea la información de los trabajadores para verla como quiero
def get_workers_today_grouped():
    rows = get_workers_today()
    grouped = {}

    for name, time, reason in rows:
        if name not in grouped:
            grouped[name] = []
        grouped[name].append({
            "time": time,
            "reason": reason
        })

    return grouped

# Facturación del día
def get_billing_today():
    query = "SELECT SUM(total) FROM appointments AS a JOIN receipts AS b ON a.id_appointment = b.id_appointment WHERE DATE(a.date_time)=%s"
    billing_today = request_bbdd(query, (today,))

    billing_today = int(billing_today[0][0])

    return billing_today

def information_today():

    data = {
        "Número de citas": get_appointments_today(),
        "Trabajadores": get_workers_today_grouped(),
        "Facturación": get_billing_today()
    }

    file_path = f"{today}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    if os.path.exists(file_path):
        print("File created")
    else:
        print("Error creating the file")