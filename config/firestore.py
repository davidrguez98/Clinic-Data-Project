import os
from dotenv import load_dotenv

load_dotenv()

FIRESTORE_CONFIG = {

    "credentials_path": os.getenv("FIRESTORE_CREDENTIALS_PATH")

}