import firebase_admin
from fastapi import UploadFile
from firebase_admin import credentials, storage
import os


# Inicializar la aplicación Firebase
base_dir = os.path.dirname(os.path.dirname(__file__))
key_path = os.path.join(base_dir, f"db\keys\serviceAccountKey.json")

cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gestplay-a56ee.appspot.com'
})

def upload_to_firebase(file: UploadFile, destination_blob_name):
    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()

    return blob.public_url


