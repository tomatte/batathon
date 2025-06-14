from sqlalchemy.orm import Session
from chatbot.clients.database import Database
from fastapi import Request
from typing import Generator

def get_db(request: Request) -> Generator[Session, None, None]:
    """Get database session from FastAPI app state."""
    db: Database = request.app.state.db
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()