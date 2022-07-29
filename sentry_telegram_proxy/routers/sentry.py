import fastapi
from dependency_injector.wiring import Provide, inject
from pydantic import ValidationError

from ..containers import AppContainer
from ..schemas.payload import Payload
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
    raw_payload: dict,
    telegram_service: TelegramService = fastapi.Depends(Provide[AppContainer.telegram]),
    sentry_service: SentrySrvice = fastapi.Depends(Provide[AppContainer.sentry]),
):
    await telegram_service.validate_webhook(webhook_id)

    try:
        payload = Payload(**raw_payload)
    except ValidationError as err:
        await telegram_service.send_document(webhook_id, raw_payload)
        return {"result": err.errors()}
    else:
        await telegram_service.send_message(webhook_id, payload)
        return {"result": "OK"}

    # await sentry_service.validate_request(request)
