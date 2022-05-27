from fastapi import APIRouter

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


@router.get("/get")
def get_users():
    return {"users": ["Jano", "Fero"]}
