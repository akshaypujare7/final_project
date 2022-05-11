import io
import logging
from flask import url_for

from app import db
from app.db.models import User, Transaction


def test_csv_upload(client):
    """This tests for successful upload of csv and processed"""
    log = logging.getLogger("CSV_upload")
    file_name = "test-stream.csv"
    data = {
        'image': (io.BytesIO(b"data"), file_name)
    }
    response = client.post('/transactions/upload', data=data)
    log.info('Test to check csv upload')
    assert response.status_code == 400


def test_csv_upload_access_denied(client):
    with client:
        """This tests for checking if access to songs upload page is denied without login"""
        response = client.get("/transactions/upload")
        assert response.status_code == 302
        response_csv = client.get("/transactions/upload", follow_redirects=True)
        assert response_csv.request.path == url_for('auth.login')
        assert response_csv.status_code == 200