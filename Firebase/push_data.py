import firebase_admin
from firebase_admin import credentials, firestore
import json

def push_data():
    # Initialize Firestore with your credentials from the environment variable
    cred = credentials.Certificate("C:\Projects\scholarships-8b654-firebase-adminsdk-k46ev-88c20f7958.json")
    firebase_admin.initialize_app(cred)

    # Access Firestore
    db = firestore.client()

    # Read data from the JSON file
    json_file_path = 'scholarships_data.json'  # Replace with the correct file path
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_content = file.read()
            data = json.loads(json_content)

        # Reference to 'scholarships' collection
        scholarships_ref = db.collection('scholarships')

        # Delete existing documents in 'scholarships' collection
        existing_docs = scholarships_ref.stream()  # Fetch all documents in collection
        c = 0
        for doc in existing_docs:
            doc.reference.delete()  # Delete each document
            c+=1
            if c%10 == 0:
                print("Please wait, deleting existing data from cloud firestore...")

        # Push new data to Firestore
        c = 0
        for entry in data:
            doc_ref = scholarships_ref.document()
            doc_ref.set(entry)  # Set each entry in the collection

            c+=1
            if c%10 == 0:
                print("Please wait, pushing data to cloud firestore...")

        print("New data has been pushed to Firestore, replacing existing documents")
    except Exception as e:
        print('Error with pushing data:', e)

push_data()