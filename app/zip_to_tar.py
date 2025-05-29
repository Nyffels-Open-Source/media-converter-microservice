import zipfile
import tarfile
import os
from fastapi import UploadFile
from tempfile import NamedTemporaryFile

def convert_zip_to_tar(uploaded_file: UploadFile) -> str:
    # Opslaan van het geüploade bestand als tijdelijk ZIP-bestand
    with NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
        temp_zip.write(uploaded_file.file.read())
        temp_zip_path = temp_zip.name

    # Voorbereiden van het output TAR-bestandspad
    base_name = os.path.splitext(os.path.basename(temp_zip_path))[0]
    output_dir = "/tmp/media"
    os.makedirs(output_dir, exist_ok=True)
    tar_path = os.path.join(output_dir, f"{base_name}.tar")

    # Extract & convert
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        temp_extract_path = os.path.join(output_dir, "temp_extract")
        os.makedirs(temp_extract_path, exist_ok=True)
        zip_ref.extractall(temp_extract_path)

        with tarfile.open(tar_path, 'w') as tar_ref:
            for root, _, files in os.walk(temp_extract_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, temp_extract_path)
                    tar_ref.add(full_path, arcname=arcname)

    os.remove(temp_zip_path)
    return tar_path
