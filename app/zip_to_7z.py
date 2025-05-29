import os
import uuid
import shutil
import zipfile
import subprocess
from fastapi import UploadFile, HTTPException

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_zip_to_7z(file: UploadFile) -> str:
    zip_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.zip")
    sevenz_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.7z")

    with open(zip_path, "wb") as f:
        f.write(file.file.read())

    try:
        result = subprocess.run([
            "7z", "a", "-t7z", sevenz_path, zip_path
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"ZIP to 7z conversion failed: {e.stderr.decode()}")

    return sevenz_path
