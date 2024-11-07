import os

import fastapi

from api.control.connector import get_controller

from model.Course import Course


router = fastapi.APIRouter(prefix="/course", tags=[ "Course" ])

@router.post("/")
def create(course: Course) -> int:
    controller = get_controller()

    id = controller.course.create(course=course)

    if not id:
        controller.rollback()
        raise fastapi.HTTPException(status_code=500, detail="Server error.")

    controller.commit()

    return id

@router.put("/{id}")
def update(id: int, course: Course) -> bool:
    controller = get_controller()

    was_updated = controller.course.update(id=id, course=course)

    controller.commit()

    return was_updated

@router.delete("/{id}")
def delete(id: int) -> bool:
    controller = get_controller()

    was_deleted = controller.course.delete(id=id)

    controller.commit()

    return was_deleted

@router.get("/{uid}")
def get_all_from_uid(uid: int) -> list[Course]:
    controller = get_controller()

    return controller.course.get_all_from_uid(uid=uid)

@router.get("/search/")
def search_by_text(query: str) -> list[Course]:
    controller = get_controller()

    return controller.course.search_by_text(query=query)
