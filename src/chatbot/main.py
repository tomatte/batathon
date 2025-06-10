# ruff: noqa: E402
from dotenv import load_dotenv
load_dotenv()

from chatbot.routers.test_router import test_router
from chatbot.singletons.fast_agent_singleton import fast_agent_singleton
from fastapi import FastAPI
from contextlib import asynccontextmanager
from chatbot.routers.meta_router import meta_router
from chatbot.routers.evolution_router import evolution_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    fast = fast_agent_singleton.fast
    async with fast.run() as agent_app:
        fast_agent_singleton.set_app(agent_app)
        yield
        #shutdown
        fast_agent_singleton.set_app(None)

app = FastAPI(lifespan=lifespan, root_path="/chatbot")
app.include_router(meta_router)
app.include_router(evolution_router)
app.include_router(test_router)

@app.get("/")
def read_root():
    return {"message": "Chatbot API is running"}
