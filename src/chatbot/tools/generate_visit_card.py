from pathlib import Path
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from playwright.async_api import async_playwright
import os, time, logging
import base64
from starlette.middleware.base import BaseHTTPMiddleware

ROOT_DIR = Path(__file__).parent.parent.parent.parent
templates = Jinja2Templates(directory=f"{ROOT_DIR}/templates")

class ServiceWorker(BaseModel):
    name: str
    services_offered: str
    services_count: int = 10
    rating: float = 4.5



async def _get_card_html(user: ServiceWorker):
    template = templates.get_template("visit_card.html")
    return template.render(user=user)
        
def _img_to_b64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode("utf-8")

    return base64_str


async def get_card_base64(html: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(args=["--no-sandbox"])
            page = await browser.new_page(viewport={"width":100,"height":100})
            await page.set_content(html, wait_until="networkidle")
            os.makedirs("prints", exist_ok=True)
            file_path = os.path.join("prints", f"cartao_{int(time.time())}.png")
            await page.screenshot(path=file_path, full_page=True)
            logging.info("Screenshot salvo em %s", file_path)
            await browser.close()
            return _img_to_b64(file_path)
    except Exception:
        logging.exception("Falha ao gerar screenshot")

async def generate_visit_card(user: ServiceWorker) -> str:
    html = await _get_card_html(user)
    return await get_card_base64(html)
