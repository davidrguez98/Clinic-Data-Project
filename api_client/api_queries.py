import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Función para recoger la información de cada endpoint
def get_api_data(endpoint: str):

    try:
        response = requests.get(f"{os.getenv("API_URL")}/{endpoint}")

        if not response:
            print("Error")
            return

        return response.json()
    except Exception as error:
        print(f"Error during the request: {error}")

def get_appointments_today():

    response = get_api_data("appointments")

    print(response)

    for data in response:
        print(data["date_time"])

get_appointments_today()

# HASTA QUE NO PONGA EL JSON BIEN NO PUEDO RECOGER LO QUE QUIERO