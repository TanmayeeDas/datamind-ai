import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.services.file_reader import read_uploaded_file
from app.services.file_cache import (
    store_dataframe,
    get_dataframe,
    get_filename
)
from app.services.dataframe_analyzer import analyze_dataframe


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


UPLOAD_DIRECTORY = "uploads"


class FileQuestionRequest(BaseModel):
    question: str


@router.post("/file")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided."
        )

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in [".csv", ".xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are supported."
        )

    os.makedirs(
        UPLOAD_DIRECTORY,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_DIRECTORY,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:

        dataframe = read_uploaded_file(
            file_path
        )

        store_dataframe(
            dataframe,
            file.filename
        )

        return {
            "filename": file.filename,
            "rows": len(dataframe),
            "columns": list(dataframe.columns)
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Could not read file: {str(e)}"
        )


@router.get("/info")
def get_uploaded_file_info():

    dataframe = get_dataframe()
    filename = get_filename()

    if dataframe is None:

        raise HTTPException(
            status_code=404,
            detail="No file has been uploaded."
        )

    return {
        "filename": filename,
        "rows": len(dataframe),
        "columns": list(dataframe.columns)
    }


@router.post("/ask")
def ask_uploaded_file(request: FileQuestionRequest):

    dataframe = get_dataframe()

    if dataframe is None:

        raise HTTPException(
            status_code=404,
            detail="Please upload a CSV or Excel file first."
        )

    try:

        result = analyze_dataframe(
            dataframe,
            request.question
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"Could not analyze the file: {str(e)}"
        )