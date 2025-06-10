from chatbot.clients.db_message_client import DBMessageClient

_db_message_client = None

def get_db_message_client() -> DBMessageClient:
    global _db_message_client
    if _db_message_client is None:
        _db_message_client = DBMessageClient()
    return _db_message_client
