"""
Basic unit test for the reasoning agent skeleton.
"""
import pytest
from reasoning_agent.core import Core
from orchestrator.runner import EchoPlugin


def test_core_echo():
    c = Core({'name': 'test'})
    c.register_plugin(EchoPlugin())
    out = c.run({'input': 'ping'})
    assert 'echo' in out
    assert 'ping' in out['echo']
