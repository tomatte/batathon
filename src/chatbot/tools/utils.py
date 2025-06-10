from chatbot.models.evolution_webhook import WebhookPayload


def ensure_ninth_digit(phone: str) -> str:
    """
    Garante que o número de celular brasileiro possui o dígito 9 após o DDD.
    """
    if not phone.startswith("55") or len(phone) < 12:
        return phone  # Não é um número nacional válido, retorna como está

    country_code = phone[:2]
    ddd = phone[2:4]
    number = phone[4:]

    # Se já tem 9 dígitos e começa com 9, retorna como está
    if len(number) == 9 and number.startswith("9"):
        return phone
    # Se tem 8 dígitos, adiciona o 9
    if len(number) == 8:
        return f"{country_code}{ddd}9{number}"
    # Se tem mais de 9 dígitos, retorna como está (pode ser fixo ou já válido)
    return phone

def extract_phone_number(webhook_payload: WebhookPayload) -> str:
    jid = webhook_payload.data.key.remote_jid
    phone_number = jid.split("@")[0]
    return ensure_ninth_digit(phone_number)