# tests/test_main.py
import os
from fastapi.testclient import TestClient
from backend.api import app  # Assurez-vous que le chemin est correct
import shutil
import tempfile

client = TestClient(app)

# Configuration des dossiers temporaires pour les tests
UPLOAD_DIR = tempfile.mkdtemp()
OUTPUT_DIR = tempfile.mkdtemp()

# Fonction de nettoyage après les tests
def teardown_module(module):
    shutil.rmtree(UPLOAD_DIR)
    shutil.rmtree(OUTPUT_DIR)

def test_denoise():
    # Créer un fichier audio temporaire
    test_file_path = os.path.join(UPLOAD_DIR, "test_audio.wav")
    with open(test_file_path, "wb") as f:
        f.write(b"Dummy audio content")

    # Ouvrir le fichier en mode binaire pour le test
    with open(test_file_path, "rb") as f:
        response = client.post("/denoise/", files={"file": ("test_audio.wav", f, "audio/wav")})

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/opus"
    assert "attachment" in response.headers["content-disposition"]
