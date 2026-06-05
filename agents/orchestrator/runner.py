"""
A lightweight orchestrator runner example.
"""
from reasoning_agent.core import Core, AgentPlugin


class EchoPlugin(AgentPlugin):
    def handle(self, context):
        context['echo'] = f"Echo: {context.get('input', '')}"
        return context


if __name__ == '__main__':
    c = Core({'name': 'test-core'})
    c.register_plugin(EchoPlugin())
    out = c.run({'input': 'hello world'})
    print(out)
