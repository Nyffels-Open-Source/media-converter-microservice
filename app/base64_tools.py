import base64
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel


async def convert_file_to_base64(file: UploadFile):
    content = await file.read()
    encoded = base64.b64encode(content).decode("utf-8")

    metadata = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }

    return {"base64": encoded, "metadata": metadata}


async def convert_file_to_base64_datastring(file: UploadFile):
    content = await file.read()
    encoded = base64.b64encode(content).decode("utf-8")
    datastring = f"data:{file.content_type};base64,{encoded}"
    return {"data_uri": datastring}


class Base64FileInput(BaseModel):
    base64: str
    filename: str
    content_type: str = "application/octet-stream"


def convert_base64_to_file(input: Base64FileInput):
    binary_data = base64.b64decode(input.base64)
    return Response(
        content=binary_data,
        media_type=input.content_type,
        headers={"Content-Disposition": f'attachment; filename="{input.filename}"'}
    )


class Base64DataURIInput(BaseModel):
    data_uri: str
    filename: str


def convert_datauri_to_file(input: Base64DataURIInput):
    if not input.data_uri.startswith("data:"):
        raise HTTPException(status_code=400, detail="Invalid data URI format")

    try:
        header, encoded = input.data_uri.split(",", 1)
        content_type = header.split(";")[0][5:]
        binary_data = base64.b64decode(encoded)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid data URI")

    return Response(
        content=binary_data,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{input.filename}"'}
    )
