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
    real_audio_path = "/home/mendo/Downloads/PROJETS_5/audio_denoising_app/data/b1.wav"

    # Ouvrir le fichier en mode binaire pour le test
    with open(real_audio_path, "rb") as f:
        response = client.post("/denoise/", files={"file": ("b1.wav", f, "audio/wav")})

    # Vérifie la réponse
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/opus"
    assert "attachment" in response.headers["content-disposition"]