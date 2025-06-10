from threading import Lock
from mcp_agent import AgentApp, FastAgent


class _FastAgentSingleton:
    _app: AgentApp | None = None
    _instance = None
    _lock = Lock()
    _fast: FastAgent | None = None
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            else:
                raise Exception("FastAgentSingleton already instanciated")
        return cls._instance
    
    def set_app(self, agent_app: AgentApp | None):
        self._app = agent_app

    @property
    def app(self) -> AgentApp:
        if not isinstance(self._app, AgentApp):
            raise Exception("Agent app not initialized.")
        return self._app
    
    @property
    def fast(self) -> FastAgent:
        if self._fast is None:
            self._fast = FastAgent("API Agent")

        return self._fast
    
fast_agent_singleton = _FastAgentSingleton()