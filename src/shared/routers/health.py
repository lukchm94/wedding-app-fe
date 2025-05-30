from typing import TypedDict

from fastapi import APIRouter, status


class HealthResponse(TypedDict):
    status: str


router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthResponse,
    description="API Health Check. Endpoint returns the dict response if the app is running",
    summary="API Health Check",
)
async def check_health() -> HealthResponse:
    return {"status": "healthy"}
