import pytest
from unittest.mock import patch, MagicMock
from typing import List, Dict
from google.cloud.firestore_v1 import Client, CollectionReference, WriteBatch
from Firebase.push_data import clear_collection, initialize_firestore, batch_upload, push_scholarship_data


@pytest.fixture
def sample_data() -> List[Dict[str, str]]:
    """
    Fixture providing example data for Firestore upload.

    Returns:
        List[Dict[str, str]]: Mocked list of scholarship records.
    """
    return [{"Title": "Scholarship A", "Organizer": "Org A", "Link": "http://example.com"}]


@patch("push_data.getenv", return_value="mock/path/to/creds.json")
@patch("push_data.Certificate")
@patch("push_data.initialize_app")
@patch("push_data.firestore.client")
def test_initialize_firestore(
    mock_client: MagicMock,
    mock_init: MagicMock,
    mock_cert: MagicMock,
) -> None:
    """
    Test if Firestore client is initialized correctly.
    """
    client: Client = initialize_firestore()
    mock_cert.assert_called_once()
    mock_init.assert_called_once()
    mock_client.assert_called_once()
    assert client == mock_client()


@patch.object(CollectionReference, "document")
@patch.object(CollectionReference, "stream")
def test_clear_collection(mock_stream: MagicMock, mock_document: MagicMock) -> None:
    """
    Test clearing of Firestore collection.

    Args:
        mock_stream (MagicMock): Mocked stream method.
        mock_document (MagicMock): Mocked document method.
    """
    fake_doc: MagicMock = MagicMock()
    fake_doc.id = "123"
    mock_stream.return_value = [fake_doc]

    fake_delete = MagicMock()
    mock_document.return_value = fake_delete

    collection: CollectionReference = MagicMock(spec=CollectionReference)
    clear_collection(collection)

    mock_document.assert_called_with("123")
    fake_delete.delete.assert_called_once()


@patch("push_data.WriteBatch", autospec=True)
def test_batch_upload(mock_write_batch_cls: MagicMock) -> None:
    """
    Test that Firestore batch upload works and commits correctly.
    """
    # Sample data
    sample_data: List[Dict[str, str]] = [
        {"Title": "Test Scholarship", "From": "TestSource"}
    ]

    # Create mocks
    mock_batch: MagicMock = MagicMock(spec=WriteBatch)
    mock_write_batch_cls.return_value = mock_batch

    client: Client = MagicMock()
    collection: CollectionReference = MagicMock()

    client.batch.return_value = mock_batch

    batch_upload(client, collection, sample_data, batch_size=1)

    assert mock_batch.set.called
    assert mock_batch.commit.called


@patch("push_data.initialize_firestore")
@patch("push_data.clear_collection")
@patch("push_data.batch_upload")
def test_push_scholarship_data(
    mock_upload: MagicMock,
    mock_clear: MagicMock,
    mock_init: MagicMock,
    sample_data: List[Dict[str, str]]
) -> None:
    """
    Test the end-to-end data push to Firestore pipeline.
    """
    mock_client: Client = MagicMock(spec=Client)
    mock_init.return_value = mock_client

    push_scholarship_data(sample_data)

    mock_clear.assert_called_once()
    mock_upload.assert_called_once()
