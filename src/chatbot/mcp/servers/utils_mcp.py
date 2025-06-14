from chatbot.factories.whatsapp_client_factory import get_evolution_client
from chatbot.clients.database import Database
from chatbot.models.schemas import JobType, ServiceOrder, User
from fastmcp import FastMCP
from sqlmodel import select
from sqlalchemy.orm import selectinload

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
def find_services() -> str:
    """Find a service."""
    db = Database()
    session = db.get_session()
    service = session.exec(select(ServiceOrder)).all()
    services_description = [{"id": service.id, "description": service.description} for service in service]
    if service:
        return f"Services found: {services_description}"  
    else:
        return f"No services found"

@mcp.tool()
async def accept_service(worker_phone: str, service_id: int) -> str:
    """Accept a service or job."""
    db = Database()
    session = db.get_session()
    statement = select(ServiceOrder).options(selectinload(ServiceOrder.user)).where(ServiceOrder.id == service_id)
    service = session.exec(statement).first()
    phone_plus = f"+{service.user.phone}"
    message = f"""
        Seu serviço foi aceito. Obrigado por usar o nosso serviço.
        Entre em contato com o profissional para agendar o serviço.

        O número de {service.user.name} é {worker_phone}, pode entrar em contato com ele para agendar o serviço.
    """
    evolution_client = get_evolution_client()
    await evolution_client.send_text_message(phone_plus, message)
    return f"Serviço '{service.description}' aceito com sucesso. Avise o usuário que seu número foi enviado para o contratante."
