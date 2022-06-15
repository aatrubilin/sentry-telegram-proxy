import fastapi
from dependency_injector.wiring import Provide, inject

from ..containers import AppContainer
from ..services import SentrySrvice, TelegramService

router = fastapi.APIRouter(prefix="/products", tags=["products"])


@router.post(
    "/sentry/{webhook_id}",
    status_code=fastapi.status.HTTP_201_CREATED,
)
@inject
async def webhook(
    request: fastapi.Request,
    webhook_id: str,
    payload: dict,
    telegram_service: TelegramService = fastapi.Depends(Provide[AppContainer.telegram]),
    sentry_service: SentrySrvice = fastapi.Depends(Provide[AppContainer.sentry]),
):
    await telegram_service.validate_webhook(webhook_id)
    # await sentry_service.validate_request(request)
    await telegram_service.send_message(webhook_id, payload)
    return {"result": "OK"}
