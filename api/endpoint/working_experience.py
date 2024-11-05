import os

import fastapi

from api.control.connector import get_controller

from model.WorkingExperience import WorkingExperience


router = fastapi.APIRouter(prefix="/working-experience", tags=[ "WorkingExperience" ])

@router.post("/")
def create(working_experience: WorkingExperience) -> int:
    controller = get_controller()

    id = controller.working_experience.create(working_experience=working_experience)

    if not id:
        controller.rollback()
        raise fastapi.HTTPException(status_code=500, detail="Server error.")

    controller.commit()

    return id

@router.put("/{id}")
def update(id: int, working_experience: WorkingExperience) -> bool:
    controller = get_controller()

    was_updated = controller.working_experience.update(id=id, working_experience=working_experience)

    controller.commit()

    return was_updated

@router.delete("/{id}")
def delete(id: int) -> bool:
    controller = get_controller()

    was_deleted = controller.working_experience.delete(id=id)

    controller.commit()

    return was_deleted

@router.get("/{uid}")
def get_all_from_uid(uid: int) -> list[WorkingExperience]:
    controller = get_controller()

    return controller.working_experience.get_all_from_uid(uid=uid)

@router.get("/search/")
def search_by_text(query: str) -> list[WorkingExperience]:
    controller = get_controller()

    return controller.working_experience.search_by_text(query=query)
