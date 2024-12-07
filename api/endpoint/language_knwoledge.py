import os

import fastapi

from api.control.connector import get_controller

from model.LanguageKnowledge import LanguageKnowledge, LanguageProciencyLevel


router = fastapi.APIRouter(prefix="/language_knowledge", tags=[ "LanguageKnowledge" ])

@router.post("/")
def create(language_knowledge: LanguageKnowledge) -> int:
    controller = get_controller()

    id = controller.language_knowledge.create(language_knowledge=language_knowledge)

    if not id:
        controller.rollback()
        raise fastapi.HTTPException(status_code=500, detail="Server error.")

    controller.commit()

    return id

@router.put("/{id}")
def update(id: int, language_knowledge: LanguageKnowledge) -> bool:
    controller = get_controller()

    was_updated = controller.language_knowledge.update(id=id, language_knowledge=language_knowledge)

    controller.commit()

    return was_updated

@router.delete("/{id}")
def delete(id: int) -> bool:
    controller = get_controller()

    was_deleted = controller.language_knowledge.delete(id=id)

    controller.commit()

    return was_deleted

@router.get("/{uid}")
def get_all_from_uid(uid: int) -> list[LanguageKnowledge]:
    controller = get_controller()

    return controller.language_knowledge.get_all_from_uid(uid=uid)

@router.get("/search/")
def search_by_text(query: str, proficiency_level: LanguageProciencyLevel | None) -> list[LanguageKnowledge]:
    controller = get_controller()

    return controller.language_knowledge.search_by_text(query=query, proficiency_level=proficiency_level)
