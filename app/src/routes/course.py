from typing import List

from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from src.auth import AuthHandler
from src.db.coursedbmanager import CourseDatabaseManager
from src.models import CourseModel


auth_handler = AuthHandler()
courses_dm = CourseDatabaseManager()


router = APIRouter(
    prefix='/courses',
    tags=['courses'],
    dependencies=[Depends(auth_handler.auth_wrapper)],
)


@router.get("/", response_description="List of Courses", response_model=List[CourseModel])
async def courses():
    content = await courses_dm.get_courses()
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)


@router.post("/", response_description="Added Course", response_model=CourseModel)
async def insert_course(course: CourseModel = Body(...)):
    course = jsonable_encoder(course)
    course.update({"course_title": course["course_title"].title().replace(' Of ', ' of ').replace(' And ', ' and ')})
    course.update({"course_code": course["course_code"].upper()})
    status_code = status.HTTP_201_CREATED
    try:
        content = await courses_dm.insert_course(course)
    except:
        content = {"detail": "Course Code already exist"}
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(status_code=status_code, content=content)


# TODO: Add Update Course Endpoint


@router.delete("/{course_code}", response_description="No Content")
async def remove_course(course_code: str):
    course_code = course_code.upper()
    if await courses_dm.remove_course(course_code) == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content={"detail": f"Course Code '{course_code}' not found"}, status_code=status.HTTP_404_NOT_FOUND)
