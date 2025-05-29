import os
import uuid
import shutil
import zipfile
import subprocess
from fastapi import UploadFile, HTTPException

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_7z_to_zip(file: UploadFile) -> str:
    sevenz_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.7z")
    extract_dir = os.path.join(TEMP_DIR, f"extract_{uuid.uuid4()}")
    zip_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.zip")

    with open(sevenz_path, "wb") as f:
        f.write(file.file.read())

    os.makedirs(extract_dir, exist_ok=True)

    try:
        subprocess.run(["7z", "x", sevenz_path, f"-o{extract_dir}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, extract_dir)
                    zipf.write(full_path, arcname)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"7z to ZIP conversion failed: {e.stderr.decode()}")
    finally:
        shutil.rmtree(extract_dir, ignore_errors=True)
        os.remove(sevenz_path)

    return zip_path
