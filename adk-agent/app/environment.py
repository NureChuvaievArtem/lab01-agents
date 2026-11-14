"""Середовище агента: перевірені відомості про сутності та бізнес-правила системи SmartLease.

Детермінований код без LLM. Джерела фактів:
Специфікація архітектури SmartLease v1.0 (2026),
Модулі платформи нерухомості (Properties, Maintenance, Finance, Utilities, Auth),
Чуваєв Артем (ПЗПІ-23-3).
"""

SMARTLEASE_ENTITIES: dict[str, dict[str, str]] = {
    "property": {
        "module": "properties_module",
        "description": (
            "Житловий або комерційний об'єкт нерухомості (квартира, офіс, паркомісце) "
            "із закріпленою адресою, площею, технічними характеристиками, базовою орендною ставкою "
            "та статусом (available, rented, maintenance, locked). "
            "Центральна сутність обліку фонду нерухомості в модулі Properties."
        ),
    },
    "lease_agreement": {
        "module": "properties_module",
        "description": (
            "Юридичний договір оренди між орендодавцем та орендарем на визначений строк "
            "із зазначенням місячної плати, обов'язкового гарантійного депозиту, дня платежу "
            "та статусу (draft, active, terminated, expired). "
            "Пов'язаний з конкретним об'єктом нерухомості та профілем орендаря."
        ),
    },
    "maintenance_request": {
        "module": "maintenance_module",
        "description": (
            "Заявка на плановий або аварійний ремонт приміщення із категорією несправності, "
            "рівнем пріоритету (low, medium, high, urgent), лімітом кошторису та життєвим циклом "
            "статусів (submitted, assigned, in_progress, resolved, cancelled). "
            "Фіксує взаємодію з підрядниками в модулі Maintenance."
        ),
    },
    "payment": {
        "module": "finance_module",
        "description": (
            "Фінансова транзакція нарахування або сплати оренди чи комунальних послуг "
            "із фіксованою сумою NUMERIC(12, 2), методом розрахунку та статусом "
            "(pending, completed, failed, refunded). "
            "Інтегрована з договором оренди та банківським шлюзом у модулі Finance."
        ),
    },
    "meter_reading": {
        "module": "utilities_module",
        "description": (
            "Показник лічильника комунальних послуг (вода, електроенергія, газ, опалення) "
            "для конкретного об'єкта нерухомості із зафіксованим числовим значенням, датою передачі "
            "та статусом перевірки. "
            "Використовується модулем Utilities для автоматичного виставлення рахунків."
        ),
    },
    "tenant_profile": {
        "module": "auth_module",
        "description": (
            "Профіль орендаря з верифікованими контактами, історією оплат, "
            "кредитним рейтингом платоспроможності та переліком укладених договорів оренди. "
            "Зберігається у модулі Auth & Tenant Management."
        ),
    },
}

MODULE_NAMES: dict[str, str] = {
    "properties_module": "Модуль нерухомості та договорів оренди",
    "maintenance_module": "Модуль технічного обслуговування та ремонтів",
    "finance_module": "Фінансовий модуль нарахувань та платежів",
    "utilities_module": "Модуль комунальних послуг та лічильників",
    "auth_module": "Модуль автентифікації та профілів користувачів",
}

NOT_FOUND = "NOT_FOUND"


def normalize_name(name: str) -> str:
    """Зводить 'Lease Agreement', 'lease_agreement', 'lease-agreement' до канонічного ключа."""
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def lookup_smartlease_entity(name: str) -> str:
    """Return verified information about one SmartLease architectural entity.

    Use it when the user asks about a specific entity such as
    property, lease_agreement, maintenance_request, payment, meter_reading or tenant_profile.

    Args:
        name: identifier of the entity, for example "property" or "lease_agreement".

    Returns:
        "<id>: <description>" or a line starting with NOT_FOUND.
    """
    key = normalize_name(name)
    if key not in SMARTLEASE_ENTITIES:
        return f"{NOT_FOUND}: no verified information about '{name}' in SmartLease specification."
    data = SMARTLEASE_ENTITIES[key]
    return f"{key}: {data['description']} [Модуль: {data['module']}]"


def list_entities_by_module(module: str) -> str:
    """Return all SmartLease entities belonging to the given functional module.

    Use it when the user asks which entities belong to a module or explores a specific subsystem.

    Args:
        module: module identifier (e.g. 'properties_module', 'maintenance_module', 'finance_module', 'utilities_module', 'auth_module').

    Returns:
        Comma-separated list of entities or a NOT_FOUND line.
    """
    key = normalize_name(module)
    matched = [
        name
        for name, data in SMARTLEASE_ENTITIES.items()
        if normalize_name(data["module"]) == key
    ]
    if not matched:
        return f"{NOT_FOUND}: module '{module}' not found. Available modules: {', '.join(sorted(MODULE_NAMES.keys()))}."
    return f"{key} entities: {', '.join(sorted(matched))}"


def list_all_entities() -> str:
    """Return identifiers of all SmartLease entities known to the environment."""
    return ", ".join(sorted(SMARTLEASE_ENTITIES.keys()))
