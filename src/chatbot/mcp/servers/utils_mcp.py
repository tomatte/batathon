from chatbot.clients.database import Database
from chatbot.models.schemas import User
from fastmcp import FastMCP
from sqlmodel import select

mcp = FastMCP(name="MyServer")

@mcp.tool()
def get_user_info(phone: str) -> str:
    """Get user info by phone."""
    db = Database()
    session = db.get_session()
    user = session.exec(select(User).where(User.phone == phone)).first()
    if user:
        return f"User info for {phone}: {user.name}"
    else:
        return f"User not found for {phone}"