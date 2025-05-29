import os
import tempfile
import subprocess
from fastapi import UploadFile

def convert_xlsx_to_pdf(file: UploadFile) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, file.filename)

        with open(input_path, "wb") as f:
            f.write(file.file.read())

        result = subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", tmpdir,
            input_path
        ], capture_output=True)

        if result.returncode != 0:
            raise RuntimeError(f"LibreOffice conversion failed: {result.stderr.decode()}")

        # Nieuw: bepaal juiste output path
        basename_no_ext = os.path.splitext(file.filename)[0]
        output_path = os.path.join(tmpdir, f"{basename_no_ext}.pdf")

        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Output PDF was not created at {output_path}.\nSTDOUT:\n{result.stdout.decode()}\nSTDERR:\n{result.stderr.decode()}")

        final_output_path = "/tmp/" + os.path.basename(output_path)
        os.rename(output_path, final_output_path)
        return final_output_path
