import os
import uuid
import shutil
import zipfile
import tarfile
from fastapi import UploadFile, HTTPException

TEMP_DIR = "/tmp/media"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_tar_to_zip(file: UploadFile) -> str:
    tar_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.tar")
    zip_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.zip")
    extract_dir = os.path.join(TEMP_DIR, f"extract_{uuid.uuid4()}")
    os.makedirs(extract_dir, exist_ok=True)

    with open(tar_path, "wb") as f:
        f.write(file.file.read())

    try:
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(extract_dir)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, extract_dir)
                    zipf.write(full_path, arcname)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TAR to ZIP conversion failed: {str(e)}")
    finally:
        shutil.rmtree(extract_dir, ignore_errors=True)
        os.remove(tar_path)

    return zip_path
