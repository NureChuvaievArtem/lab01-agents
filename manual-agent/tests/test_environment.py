from agent.environment import (
    NOT_FOUND,
    lookup_smartlease_entity,
    list_entities_by_module,
    normalize_name,
)


def test_existing_entity():
    res = lookup_smartlease_entity("property")
    assert res.startswith("property:")
    assert "properties_module" in res


def test_name_is_normalized():
    res1 = lookup_smartlease_entity("Lease Agreement")
    res2 = lookup_smartlease_entity("lease_agreement")
    res3 = lookup_smartlease_entity("lease-agreement")
    assert res1.startswith("lease_agreement:")
    assert res1 == res2 == res3


def test_unknown_entity():
    res = lookup_smartlease_entity("crypto_wallet")
    assert res.startswith(NOT_FOUND)
    assert "crypto_wallet" in res


def test_list_entities_by_module_valid():
    res = list_entities_by_module("properties_module")
    assert "lease_agreement" in res
    assert "property" in res


def test_list_entities_by_module_unknown():
    res = list_entities_by_module("ai_governance_module")
    assert res.startswith(NOT_FOUND)
