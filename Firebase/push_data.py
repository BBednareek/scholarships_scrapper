from os import getenv
from typing import List, Dict
from firebase_admin.credentials import Certificate
from firebase_admin import firestore, initialize_app
from google.cloud.firestore_v1 import Client, CollectionReference, WriteBatch
from utils.error_handler import error_handler
from dotenv import load_dotenv

@error_handler("send")
def initialize_firestore(env_file: str = ".env") -> Client:
    """
    Loads env and initializes Firestore client.

    Args:
        env_file (str): Path to .env file containing credentials.

    Returns:
        Client: Firestore client.
    """
    load_dotenv(dotenv_path=env_file)
    cred_path: str | None = getenv("FIREBASE_CREDENTIAL_PATH")
    if not cred_path:
        raise ValueError("FIREBASE_CREDENTIAL_PATH not set")
    cred: Certificate = Certificate(cred_path)
    initialize_app(cred)
    return firestore.client()

@error_handler("send")
def clear_collection(collection: CollectionReference) -> None:
    """
    Deletes all existing documents in the Firestore collection.

    Args:
        collection (CollectionReference): Target Firestore collection.
    """

    for doc in collection.stream():
        collection.document(doc.id).delete()

@error_handler("send")
def batch_upload(client: Client, collection: CollectionReference, data: List[Dict[str, str]], batch_size: int = 500) -> None:
    """
    Uploads scholarship data to Firestore in batches.

    Args:
        client (Client): Firestore client.
        collection (CollectionReference): Collection to upload into.
        data (List[Dict[str, str]]): List of scholarships.
        batch_size (int): Max docs per batch commit.
    """
    batch: WriteBatch = client.batch()
    count: int = 0
    for entry in data:
        batch.set(collection.document(), entry)
        count += 1
        if count >= batch_size:
            batch.commit()
            batch: WriteBatch = client.batch()
            count = 0
    if count:
        batch.commit()

@error_handler("send")
def push_scholarship_data(data: List[Dict[str, str]]) -> None:
    """
    Pushes scholarship data to Firestore immediately (no local storage).

    Args:
        data (List[Dict[str, str]]): Scholarships to push.
    """
    client: Client = initialize_firestore()
    coll: CollectionReference = client.collection("scholarships")
    clear_collection(coll)
    batch_upload(client, coll, data)
    print(f"Pushed {len(data)} scholarships to Firestore.")
