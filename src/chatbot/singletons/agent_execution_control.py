from typing import Dict

class _AgentExecutionControl:
    _instance = None
    _agent_states: Dict[str, bool] = {}
    _agent_names = ["jaiminho"]
    
    def __new__(cls):
        if cls._instance is not None:
            raise Exception("AgentExecutionControl already instanciated")
        cls._instance = super().__new__(cls)
        return cls._instance
    
    def can_execute(self, phone_number: str) -> bool:
        return self._agent_states.get(phone_number, None) is not None
    
    def enable_agent(self, agent_name: str, phone_number: str) -> None:
        if agent_name not in self._agent_names:
            raise Exception("Agent name not found")
        print(f"Enabling {agent_name} agent for {phone_number}")
        
        self._agent_states[phone_number] = agent_name

    def disable_agent(self, agent_name: str, phone_number: str) -> None:
        if agent_name not in self._agent_names:
            raise Exception("Agent name not found")
        print(f"Disabling {agent_name} agent for {phone_number}")
        
        self._agent_states[phone_number] = None
    
    def is_agent_enabled(self, agent_name: str, phone_number: str) -> bool:
        return self._agent_states.get(phone_number, None) == agent_name
    
    def get_agent_name(self, phone_number: str) -> str:
        agent_name = self._agent_states.get(phone_number, None)
        if agent_name is None:
            raise Exception(f"No agent enabled for {phone_number}")
        
        return agent_name

    def hello_agent(self, greeting: str, phone_number: str):
        words = greeting.lower().split()
        if len(words) != 2:
            return
        if words[0] != "oi":
            return
        if words[1] not in self._agent_names:
            return
        
        self.enable_agent(words[1], phone_number)

    def goodbye_agent(self, greeting: str, phone_number: str):
        words = greeting.lower().split()
        if len(words) != 2:
            return
        if words[0] != "tchau":
            return
        if words[1] not in self._agent_names:
            return
        
        self.disable_agent(words[1], phone_number)


agent_execution_control = _AgentExecutionControl()