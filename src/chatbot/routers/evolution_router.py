from chatbot.factories.evolution_service_factory import get_evolution_service
from chatbot.models.evolution_webhook import WebhookPayload
from chatbot.factories.whatsapp_client_factory import get_evolution_client
from chatbot.models.evolution_models import EvolutionSendText
from fastapi import APIRouter, Request, Response, status

evolution_router = APIRouter(
    prefix="/whatsapp/evolution",
    tags=["WhatsApp Evolution"]
)

@evolution_router.get("/")
def test():
    return {"message": "Evolution WhatsApp API is working"}

@evolution_router.post("/any")
async def receive_any(request: Request):
    body = await request.json()
    print("Incoming any:", body)
    return Response(status_code=status.HTTP_200_OK)

@evolution_router.post("/webhook/messages-upsert")
async def receive_messages_upsert(request: Request):
    body = await request.json()
    print("Incoming send text:\n\n", body)
    print("\n--------------------------------\n")
    webhook_payload = WebhookPayload(**body)
    service = get_evolution_service()
    await service.process(webhook_payload)
    return Response(status_code=status.HTTP_200_OK)

@evolution_router.post("/trigger/send_text")
async def send_text(send_text_request: EvolutionSendText):
    print("Incoming send text:", send_text_request.message)
    whatsapp_client = get_evolution_client()
    await whatsapp_client.send_text_message(send_text_request.number, send_text_request.message)
    return Response(status_code=status.HTTP_200_OK)
