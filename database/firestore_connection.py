import firebase_admin
from firebase_admin import credentials, firestore
from config.firestore import FIRESTORE_CONFIG

class FirestoreConnection:
    
    def __init__(self):
        self.db = None
        self._initialize_firestore()

    def _initialize_firestore(self):

        try:
            # Verificación de que se ha inicializado
            if not firebase_admin._apps:
                cred = credentials.Certificate(FIRESTORE_CONFIG["credentials_path"])
                firebase_admin.initialize_app(cred)

            self.db = firestore.client()
            print("Conection established with Firestore")
        except FileNotFoundError:
            print("The credentials file wasn't founded")
            raise
        except Exception as error:
            print(f"Error during the connection: {error}")
            raise

    def get_client(self):
        # Devuelve el cliente de Firestore
        if self.db is None:
            raise Exception("The connection to Firestore is not initialized")
        return self.db
