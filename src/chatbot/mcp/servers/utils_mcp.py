from chatbot.factories.whatsapp_client_factory import get_evolution_client
from chatbot.clients.database import Database
from chatbot.models.schemas import JobType, ServiceOrder, User, UserServiceOrderLink
from chatbot.tools.generate_visit_card import generate_visit_card
from chatbot.tools.utils import ensure_ninth_digit
from fastmcp import FastMCP
from sqlmodel import select
from sqlalchemy.orm import selectinload
import logging

logging.basicConfig(level=logging.INFO)
mcp = FastMCP(name="MyServer")

@mcp.tool()
def get_user_info(phone: str) -> str:
    """Get user info by phone."""
    phone = ensure_ninth_digit(phone)
    db = Database()
    session = db.get_session()
    user = session.exec(select(User).where(User.phone == phone)).first()
    if user:
        return user.model_dump(include={"name", "phone"})
    else:
        return f"User not found for {phone}"
    
@mcp.tool()
def create_user(phone: str, name: str) -> str:
    """Create a new user with just name and phone."""
    db = Database()
    session = db.get_session()
    user = session.exec(select(User).where(User.phone == phone)).first()
    if user:
        return f"User already exists for {phone}"
    else:
        user = User(phone=phone, name=name)
        session.add(user)
        session.commit()
        return f"User created for {phone}"

@mcp.tool()
async def register_willing_job(phone: str, job_description: str) -> str:
    """Register or update the user profession, the type of jobs he wants to do and services he wants to offer"""
    db = Database()
    session = db.get_session()
    user = session.exec(select(User).where(User.phone == phone)).first()
    if not user:
        return f"User not found for {phone}"
    
    await get_evolution_client().send_text_message(phone, "Serviço registrado com sucesso")
    
    job_type_obj = JobType(description=job_description)
    user.willing_jobs.append(job_type_obj)
    session.add(user)
    session.commit()
    return f"Job registered for {phone}"

@mcp.tool()
def order_a_service(phone: str, service_description: str) -> str:
    """Order a service or update existing service order."""
    db = Database()
    session = db.get_session()
    user = session.exec(select(User).where(User.phone == phone)).first()
    if not user:
        return f"User not found for {phone}"
    
    # Check if user already has a service order
    existing_link = session.exec(
        select(UserServiceOrderLink)
        .where(UserServiceOrderLink.user_id == user.id)
    ).first()
    
    if existing_link:
        # Update existing service order
        service_order = session.exec(
            select(ServiceOrder)
            .where(ServiceOrder.id == existing_link.service_order_id)
        ).first()
        service_order.description = service_description
        session.add(service_order)
        session.commit()
        return f"Service order updated for {phone}"
    else:
        # Create new service order
        service_order = ServiceOrder(description=service_description)
        session.add(service_order)
        session.commit()  # Commit first to get the service_order.id
        
        # Now create the link with the service_order.id
        user_service_order = UserServiceOrderLink(
            user_id=user.id,
            service_order_id=service_order.id
        )
        session.add(user_service_order)
        session.commit()
        return f"New service ordered for {phone}"

@mcp.tool()
def find_available_services() -> str:
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
    logging.info(f"Accepting service {service_id} for worker {worker_phone}")
    db = Database()
    session = db.get_session()
    statement = select(ServiceOrder).options(selectinload(ServiceOrder.user)).where(ServiceOrder.id == service_id)
    service = session.exec(statement).first()
    message = f"""
        Seu serviço foi aceito. Obrigado por usar o nosso serviço.
        Entre em contato com o profissional para agendar o serviço.

        O número de {service.user.name} é {worker_phone}, pode entrar em contato com ele para agendar o serviço.
    """
    evolution_client = get_evolution_client()
    visit_card = await generate_visit_card({
        "name": service.user.name,
        "services_offered": service.description,
        "services_count": 10,
        "rating": 4.5
    })

    await evolution_client.send_image_message(service.user.phone, visit_card, message)
    return f"Serviço '{service.description}' aceito com sucesso. Avise o usuário que seu número foi enviado para o contratante."
