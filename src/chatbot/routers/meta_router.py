from fastapi import Response, status, Request, Query, APIRouter
from chatbot.factories.whatsapp_service_factory import get_whatsapp_service


VERIFY_TOKEN = "d8a9b7td8ia7diauy"  # Replace with your actual verify token
meta_router = APIRouter(
    prefix="/whatsapp/official",
    tags=["WhatsApp Official"]
)

@meta_router.get("/")
def test():
    return {"message": "Official WhatsApp API is working"}

@meta_router.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return Response(content=hub_challenge, media_type="text/plain")
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

@meta_router.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("Incoming webhook:", body)
    whatsapp_service = get_whatsapp_service("official")
    await whatsapp_service.process(body)
    return Response(status_code=status.HTTP_200_OK)
