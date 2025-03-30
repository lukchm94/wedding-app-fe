from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    description="API Health Check. Endpoint returns the dict response if the app is running",
    summary="API Health Check",
)
async def check_health() -> dict:
    return {"status": "healthy"}
