import os

import fastapi

from api.control.connector import get_controller

from model.AcademicBackground import AcademicBackground, EducationLevel


router = fastapi.APIRouter(prefix="/academic-background", tags=[ "AcademicBackground" ])

@router.post("/")
def create(academic_background: AcademicBackground) -> int:
    controller = get_controller()

    id = controller.academic_background.create(academic_background=academic_background)

    if not id:
        controller.rollback()
        raise fastapi.HTTPException(status_code=500, detail="Server error.")

    controller.commit()

    return id

@router.put("/{id}")
def update(id: int, academic_background: AcademicBackground) -> bool:
    controller = get_controller()

    was_updated = controller.academic_background.update(id=id, academic_background=academic_background)

    controller.commit()

    return was_updated

@router.delete("/{id}")
def delete(id: int) -> bool:
    controller = get_controller()

    was_deleted = controller.academic_background.delete(id=id)

    controller.commit()

    return was_deleted

@router.get("/{uid}")
def get_all_from_uid(uid: int) -> list[AcademicBackground]:
    controller = get_controller()

    return controller.academic_background.get_all_from_uid(uid=uid)

@router.get("/search/")
def search_by_text(query: str, education_level: EducationLevel | None = None) -> list[AcademicBackground]:
    controller = get_controller()

    return controller.academic_background.search_by_text(query=query, education_level=education_level)
