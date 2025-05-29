import os
import tempfile
import subprocess
from fastapi import UploadFile

def convert_pdf_to_pdfa(file: UploadFile) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, file.filename)
        output_path = os.path.join(tmpdir, "output_pdfa.pdf")

        with open(input_path, "wb") as f:
            f.write(file.file.read())

        result = subprocess.run([
            "gs",
            "-dPDFA=2",
            "-dBATCH",
            "-dNOPAUSE",
            "-dNOOUTERSAVE",
            "-sProcessColorModel=DeviceCMYK",
            "-sDEVICE=pdfwrite",
            "-sPDFACompatibilityPolicy=1",
            f"-sOutputFile={output_path}",
            input_path
        ], capture_output=True)

        if result.returncode != 0:
            raise RuntimeError(f"Ghostscript conversion failed: {result.stderr.decode()}")

        final_output_path = "/tmp/" + os.path.basename(output_path)
        os.rename(output_path, final_output_path)
        return final_output_path
