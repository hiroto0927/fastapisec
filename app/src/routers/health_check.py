from fastapi import APIRouter

router = APIRouter()


@router.get("/health-check")
def helth_check():
    return {"msg": "hello"}
