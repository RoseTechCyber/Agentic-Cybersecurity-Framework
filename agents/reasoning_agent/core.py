"""
Core orchestrator skeleton for the reasoning agent.
"""
from typing import Any, Dict


class Core:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def run(self, input_data: Dict[str, Any]):
        # Simple orchestration loop: call each plugin in sequence
        context = input_data.copy()
        for p in self.plugins:
            context = p.handle(context)
        return context


class AgentPlugin:
    """Base class for agent plugins"""

    def handle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
