from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health() -> str:
    return "I am alive"
