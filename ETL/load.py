from database.firestore_connection import FirestoreConnection

class DataLoader:

    def __init__(self):
        self.firestone_connection = FirestoreConnection()
        self.db = self.firestone_connection.get_client()

    # Sube la información recopilada del día a Firestone
    def load_daily_information(self, data: dict):

        try:
            doc_id = data["date"]
            self.db.collection("daily_information").document(doc_id).set(data)

            print(f"Data of {doc_id} loaded correctly")
            return True
        except Exception as error:
            print(f"Error loading data into Firestore: {error}")
            return False