from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from .utils import (denoise,convert_to_wav,convert_to_opus)
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)



# API Endpoints

@app.get("/greet/")
def greet():
    return {"message": "bonjour Leo le lengendaire"}




@app.post("/denoise/")
async def api_denoise(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        denoised_path = denoise(input_path) 
        final_opus = convert_to_opus(denoised_path,OUTPUT_DIR )
        return FileResponse(final_opus, media_type="audio/opus", filename=os.path.basename(denoised_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Denoising failed: {e}")

