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

def request_bbdd(query: str):
    connection = clinic.get_connection()

    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return result

# Cantidad citas del día
def get_appointments_today():
    appointments_quantity = request_bbdd(
        f"SELECT COUNT(*) FROM appointments WHERE DATE(date_time)='{today}'"
    )

    return appointments_quantity[0][0]

# Personal de la empresa que ha trabajado
def get_workers_today():
    workers_today = request_bbdd(
        f"SELECT b.name, DATE_FORMAT(a.date_time, '%H:%i'), a.reason FROM appointments AS a JOIN workers AS b ON a.id_worker = b.id_worker WHERE DATE(a.date_time)='{today}'"
    )

    # workers_today_formatted = [
    #     {"name": worker[0], "time": worker[1], "reason": worker[2]}
    #     for worker in workers_today
    # ]

    # return workers_today_formatted
    return workers_today

# Facturación del día
def get_billing_today():
    billing_today = request_bbdd(
        f"SELECT SUM(total) FROM appointments AS a JOIN receipts AS b ON a.id_appointment = b.id_appointment WHERE DATE(a.date_time)='{today}'"
    )

    billing_today = int(billing_today[0][0])

    return billing_today

def information_today():

    data = {
        "Número de citas": get_appointments_today(),
        "Trabajadores": get_workers_today(),
        "Facturación": get_billing_today()
    }

    file_path = f"{today}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    if os.path.exists(file_path):
        print("File created")
    else:
        print("Error creating the file")

""" 
 TENGO QUE DEPURAR LA FUNCIÓN DE WORKER, YA QUE ME LO DEVUELVE POR CITAS PERO DEBERÍA DE TENER CADA TRABAJADOR UN LISTADO.

 JSON ACTÚAL:
    {
        "Número de citas": 3,
        "Trabajadores": [
            [
                "Dr. Pedro",
                "10:00",
                "Revisión anual"
            ],
            [
                "Dr. Pedro",
                "10:00",
                "Limpieza"
            ],
            [
                "Dra. Carmen",
                "11:30",
                "Ajuste ortodoncia"
            ]
        ],
        "Facturación": 250
    }
"""