from typing import List

from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from src.auth import AuthHandler
from src.db.lecturersdbmanager import LecturersDatabaseManager
from src.models import LecturerModel


auth_handler = AuthHandler()
lecturers_dm = LecturersDatabaseManager()


router = APIRouter(
    prefix='/lecturers',
    tags=['lecturers'],
    dependencies=[Depends(auth_handler.auth_wrapper)],
)


@router.get("/", response_description="List of Lecturers", response_model=List[LecturerModel])
async def lecturers():
    content = await lecturers_dm.get_lecturers()
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@router.post("/", response_description="Added Lecturer", response_model=LecturerModel)
async def insert_lecturer(lecturer: LecturerModel = Body(...)):
    lecturer = jsonable_encoder(lecturer)
    lecturer.update({"name": lecturer["name"].title()})
    lecturer.update({"code": lecturer["code"].upper()})
    status_code = status.HTTP_201_CREATED
    try:
        content = await lecturers_dm.insert_lecturer(lecturer)
    except:
        content = {"detail": "Lecturers Code already exist"}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(status_code=status_code, content=content)


# TODO: Add Update Lecturer Endpoint


@router.delete("/{lecturer_code}", response_description="No Content")
async def remove_lecturer(lecturer_code: str):
    if await lecturers_dm.remove_lecturer(lecturer_code.upper()) == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content={"detail": f"Lecturers Code '{lecturer_code}' not found"}, status_code=status.HTTP_404_NOT_FOUND)
