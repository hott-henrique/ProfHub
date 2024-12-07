import fastapi

from api.control.connector import get_controller

from model.Certificate import Certificate


router = fastapi.APIRouter(prefix="/certificate", tags=[ "Certificate" ])

@router.post("/")
def create(certificate: Certificate) -> int:
    controller = get_controller()

    id = controller.certificate.create(certificate=certificate)

    if not id:
        controller.rollback()
        raise fastapi.HTTPException(status_code=500, detail="Server error.")

    controller.commit()

    return id

@router.put("/{id}")
def update(id: int, certificate: Certificate) -> bool:
    controller = get_controller()

    was_updated = controller.certificate.update(id=id, certificate=certificate)

    controller.commit()

    return was_updated

@router.delete("/{id}")
def delete(id: int) -> bool:
    controller = get_controller()

    was_deleted = controller.certificate.delete(id=id)

    controller.commit()

    return was_deleted

@router.get("/{uid}")
def get_all_from_uid(uid: int) -> list[Certificate]:
    controller = get_controller()

    return controller.certificate.get_all_from_uid(uid=uid)

@router.get("/search/")
def search_by_text(query: str) -> list[Certificate]:
    controller = get_controller()

    return controller.certificate.search_by_text(query=query)
