import pytest
from agent.errors import DecisionError
from agent.validator import validate_decision


def test_valid_lookup():
    validate_decision({
        "action": "lookup_smartlease_entity",
        "arguments": {"name": "property"},
    })


def test_valid_list_by_module():
    validate_decision({
        "action": "list_entities_by_module",
        "arguments": {"module": "properties_module"},
    })


def test_valid_finish():
    validate_decision({
        "action": "finish",
        "arguments": {"answer": "Сутність знайдено."},
    })


@pytest.mark.parametrize("decision", [
    {"action": "delete_database", "arguments": {}},
    {"action": "lookup_smartlease_entity", "arguments": {}},
    {"action": "lookup_smartlease_entity", "arguments": {"name": 123}},
    {"action": "lookup_smartlease_entity", "arguments": {"name": "   "}},
    {"action": "finish"},
    "not_a_dict",
])
def test_invalid_decisions(decision):
    with pytest.raises(DecisionError):
        validate_decision(decision)
