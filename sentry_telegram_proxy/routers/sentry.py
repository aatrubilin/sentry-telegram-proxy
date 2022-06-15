import fastapi
from dependency_injector.wiring import Provide, inject

from ..containers import AppContainer
from ..services import TelegramService

router = fastapi.APIRouter(prefix="/products", tags=["products"])


@router.post(
    "/sentry/{webhook_id}",
    status_code=fastapi.status.HTTP_201_CREATED,
)
@inject
async def webhook(
    webhook_id: str,
    payload: dict,
    telegram_service: TelegramService = fastapi.Depends(Provide[AppContainer.telegram]),
):
    await telegram_service.send_message(payload)
    return {"result": "OK"}
