"""Тести циклу без звернень до API: рішення моделі підміняє сценарій."""
from agent.loop import run_agent


def scripted(decisions):
    queue = iter(decisions)

    def decide(goal, observations, step, max_steps):
        return next(queue)

    return decide


def test_lookup_then_finish():
    decide = scripted([
        {
            "action": "lookup_smartlease_entity",
            "arguments": {"name": "property"},
            "decision_summary": "Потрібні дані про property.",
        },
        {
            "action": "finish",
            "arguments": {"answer": "Property — базовий об'єкт нерухомості."},
            "decision_summary": "Даних достатньо.",
        },
    ])
    state = run_agent("Опиши property", decide=decide)
    assert state.stop_reason == "finish"
    assert state.llm_calls == 2
    assert state.step == 2
    assert state.observations[0].startswith("property:")


def test_stops_at_max_steps():
    def endless(goal, observations, step, max_steps):
        return {
            "action": "lookup_smartlease_entity",
            "arguments": {"name": "property"},
        }

    state = run_agent("Зациклитися", decide=endless, max_steps=3)
    assert state.stop_reason == "max_steps"
    assert state.step == 3


def test_stops_at_max_llm_calls():
    def endless(goal, observations, step, max_steps):
        return {
            "action": "lookup_smartlease_entity",
            "arguments": {"name": "property"},
        }

    state = run_agent("Ліміт викликів", decide=endless, max_steps=10, max_llm_calls=4)
    assert state.stop_reason == "max_llm_calls"
    assert state.llm_calls == 4


def test_invalid_action_becomes_observation():
    decide = scripted([
        {"action": "drop_table", "arguments": {}},
        {"action": "finish", "arguments": {"answer": "ok"}},
    ])
    state = run_agent("Тест помилки", decide=decide)
    assert state.observations[0].startswith("ERROR: unknown action")
    assert state.stop_reason == "finish"
