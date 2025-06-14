from chatbot.clients.database import Database
from chatbot.models.schemas import JobType, ServiceOrder, User
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
    
@mcp.tool()
def create_user(phone: str, name: str, job_description: str) -> str:
    """Create a new user."""
    db = Database()
    session = db.get_session()
    user = session.exec(select(User).where(User.phone == phone)).first()
    if user:
        return f"User already exists for {phone}"
    else:
        job_type_obj = JobType(description=job_description)
        user = User(phone=phone, name=name)
        user.willing_jobs.append(job_type_obj)
        session.add(user)
        session.commit()
        return f"User created for {phone}"

@mcp.tool()
def order_a_service(phone: str, service_description: str) -> str:
    """Order a service."""
    db = Database()
    session = db.get_session()
    user = session.exec(select(User).where(User.phone == phone)).first()
    if user:
        service_order = ServiceOrder(description=service_description)
        user.service_order = service_order
        session.add(user)
        session.commit()
        return f"Service ordered for {phone}"

@mcp.tool()
def find_service(service_description: str) -> str:
    """Find a service."""
    db = Database()
    session = db.get_session()
    service = session.exec(select(ServiceOrder)).all()
    services_description = [service.description for service in service]
    if service:
        return f"Services found: {services_description}"  
    else:
        return f"No services found"
