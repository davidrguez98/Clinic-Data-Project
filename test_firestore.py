from database.firestore_connection import FirestoreConnection

# Test 1 - Crear conexión
my_firestore_connection = FirestoreConnection()
print("Instancia creada")

# Test 2 - Obtener cliente

db = my_firestore_connection.get_client()
print(f"Cliente obtenido: {db}")

# Test 3 - Escribir datos de prueba

test_data = {
    "Prueba": "De conexión",
    "Fecha": "2025-11-11"
}

db.collection("prueba").document("test_doc").set(test_data)
print("Datos escritos correctamente")

# Test 4 - Leer datos de prueba

doc = db.collection("prueba").document("test_doc").get()
print(doc.to_dict())