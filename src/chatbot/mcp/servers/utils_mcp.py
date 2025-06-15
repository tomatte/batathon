from chatbot.factories.whatsapp_client_factory import get_evolution_client
from chatbot.clients.database import Database
from chatbot.models.schemas import JobType, ServiceOrder, User, UserServiceOrderLink
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
    


b64 = 'iVBORw0KGgoAAAANSUhEUgAAAVwAAAENCAIAAADMpkopAAAAAXNSR0IArs4c6QAAIABJREFUeJzt3XlYFEf6B/AabpCBRQyCihpQNMiSFVckiyKHV1Q0JJG4McYowYirySYmYvwZAY94RI0aNR5ZjUfUyOOJR1TkUCIIooKKivG+keEaQGAY+vfHu1vpnks8OJTv5/Hx6emprq6eod6uru6pkhUVFTEAgP8xaugCAEDjgqAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAggaAAABIICgAgYfJ0mwmC8LxLAgD1RCaTGXj3CYICAgHAy0Fcl7UDxOODgnYsQHQAeNHxWMCrM1/zmKAgrv/6lgHgxSKTybRjgSAItKw3KGiHAEEQjI2NzczMTExMjI2NjYzQSQnw4qmpqVGr1dXV1VVVVWq1mlZSOKCaLisqKtLejEcEcTiwsLAwNzev3/IDQB2qrKysqKhQq9UUFPS2FLQjgrm5ebNmzeq9wABQt8zNzc3NzcvKyiorK+maQiaTaQYFcUSgZQsLCysrq4YoMADUh2bNmslksoqKCnop6RfQiAiCIJiZmSEiALz0rKyszMzMqNb/GRS0I4KRkZG1tXXDlRMA6o+1tbWRkZEkKBBxaEAbAaBJsbKy+jMoaNyApGYC7jUANCnm5uZGGs8aCCKICABNkLm5uY4HkCgomJqaNkSRAKAhmZqaGomfR+C3IQVBMDF5yh9QAsCLy8TERG9LAU8xAzRBmn0KGu0FAGiCJHcfEAsAwEj7lw6IDgBNme4+hYYoCQA0CuhNBAAJ3UEBjQWAJgstBQCQ0PHTaTQTAJoytBQAQELvT6cBoGlCSwEAJOrpV08pKSmHDh1ijHXv3j04OPiJtj19+nRqamrPnj09PT1v3ry5bdu2YcOGtWvX7vmWcPv27VlZWYyxkSNHduzY8anzuX379qFDh86ePXv+/Hlra2sXFxd/f/9Bgwbx0fXz8/OXLl3KGHN2dg4PD2eMxcbGnj17ljE2atQoV1fX53dMAE+lsLCwsLCwoKBA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CwtrvwsA3eqio7GsrIw3BMRiYmJ4mtLSUnHHoVhGRgal8fHx0VfszZs3UxoebjQY6IcvLy838FgkdTROmzZNXwJxp6aYSqXSd+tBfKejlr99UKlU/DOUy+WPHj3ibx08eFDfXtq0afMsXxxAHd590Lg55+XlFR0dXV1dLU5TXl6u0Us/aNAg8c2Iq1ev8scQGGPDhg3buHEjX+bJjhw5In6EwcHBYfXq1TU1NQaK9+DBA/GTEZGRkfyZCLp3WF5ezq/hqfz8Mkcul1P11lZWVrZw4UKN30R5enr+9NNPPM3Fixc1gsIHH3xAa+Lj48W5xcTE8OJp7IiXlo5369at/IPKzs6u3VcEoJuMGpz0okakVatW+k5HtVdSUnLjxo3WrVs3b97cQLL79+8XFBR06NCB965zgiDcu3cvPz+/Q4cOVlZWBjJRqVSXLl165ZVXWrZsWcviFRcX37x5s3Pnzvpm0y0sLLx161br1q01bmE8lkKhuHnzppWVlaurax11/j169OjatWvUtamz7xPg6dRtUACAFw5uawOABIICAEggKACABIICAEggKACABIICAEggKACABIICAEggKACABIICAEggKACABIICAEggKACARF0FhfDw8FCRESNGfP3113wOpUZu/PjxkyZNMpDg9OnToaGhJ06cqOuS0GgRubm5z5LJli1bQkND+XhNz2L9+vWhoaGPHj2i6bN//fXXZ88TGpu6Cgo1NTXGxsYDBgwYMGCAn5/fq6++euXKlZkzZx47dqyO9vgc0a/IDSSwsrJycHCoh8kgz5w5s2rVqmccZI2ORefQkk+qefPmDg4ONHzD7NmzX4hvE55UHQ7+a21tLR686Pz587NmzVqxYoWHh4ednV3d7bcedOrUadmyZfWwo+dSk5+j4OBgPtcOBol9WdXfiOBdunT58MMP161bd/ToUZry6M6dOz/++OOVK1eMjIzc3d0jIiJogKbKysoVK1acPHlSpVK1aNFi8ODBAwcOpEz0bbJgwQJ7e3szM7OEhITy8vL27dt/+umnTk5Ou3btOnToUFRUFB+O6ZdffklNTf3uu+8sLS0TExNjY2Pz8/PlcnmPHj1GjRplbm7OC1xRUfHll1927dqVD+taWFj4f//3f3369OnSpcuSJUvGjx/v4eFBuzYyMkpMTFSpVD4+PhEREevWrTt27Ji5uXm/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'

@mcp.tool()
async def accept_service(worker_phone: str, service_id: int) -> str:
    """Accept a service or job."""
    logging.info(f"Accepting service {service_id} for worker {worker_phone}")
    db = Database()
    session = db.get_session()
    statement = select(ServiceOrder).options(selectinload(ServiceOrder.user)).where(ServiceOrder.id == service_id)
    service = session.exec(statement).first()

    worker = session.exec(select(User).where(User.phone == worker_phone)).first()
    
    if not service:
        return f"Service {service_id} not found"
        
    message = f"""Um novo cliente está interessado no seu serviço de {service.description}.
Entre em contato para combinar a data e hora do serviço.

Nome: {worker.name}
Número: {worker.phone}

Serviço: {service.description}
        """

    await get_evolution_client().send_text_message(worker.phone, message)
    return f"Serviço '{service.description}' aceito com sucesso. Avise o usuário que seu número foi enviado para o contratante."
