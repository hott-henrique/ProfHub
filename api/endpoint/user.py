import os

import fastapi

from api.control.connector import get_controller

from model.User import User


router = fastapi.APIRouter(prefix="/user", tags=[ "User" ])

@router.get("/{id}")
def get_by_id(id: int) -> User:
    controller = get_controller()

    u = controller.user.get_user_by_id(id=id)

    if not u:
        controller.rollback()
        raise fastapi.HTTPException(status_code=404, detail="Not Found.")

    controller.commit()

    return u

@router.put("/{id}")
def update(id: int, user: User) -> User:
    controller = get_controller()

    u = controller.user.update(id=id, user=user)

    controller.commit()

    return u

@router.delete("/{id}")
def delete(id: int) -> bool:
    controller = get_controller()

    was_deleted = controller.user.delete(id=id)

    controller.commit()

    return was_deleted

@router.get("/search/")
def search_by_text(query: str) -> list[User]:
    controller = get_controller()

    return controller.user.search_by_text(query=query)

@router.get("/most-certified/{academic_background}")
def most_certified_professionals(academic_background: str, page: int = 0, page_sz: int = 10) -> list[tuple[int, int]]:
    controller = get_controller()

    return controller.user.get_most_certified_professionals_by_academic_background(
        academic_background=academic_background,
        page=page,
        page_sz=page_sz
    )
