import logging
from collections import defaultdict

from .linter import Linter
from .builtin_rules import __all__ as rules


def find_linters_by(field: str, wanted: list[str]) -> list:
    logger = logging.getLogger(__package__)

    available = defaultdict(list)
    for linter in rules:
        if not hasattr(linter, field):
            continue
        value = getattr(linter, field)
        if isinstance(value, str):
            available[value].append(linter)
        else:
            for choice in value:
                available[choice].append(linter)

    result = []
    for chosen in wanted:
        if chosen in available:
            linters = available[chosen]
            logger.debug(f"Enabling linter{'s' if len(linters) > 1 else ''} {', '.join(linter.__name__ for linter in linters)} (from {chosen})")
            result += linters
        else:
            logger.error(f"No known linter corresponds to {chosen}")
    return result

def load_linters(config: dict) -> list[Linter]:
    logger = logging.getLogger(__package__)
    if not 'linters' in config:
        logger.error('No linter list in config')
        return []

    result = []
    linters = config['linters']

    if 'by-class' in linters:
        result += find_linters_by('__name__', linters['by-class'])
    if 'by-name' in linters:
        result += find_linters_by('name', linters['by-name'])
    if 'by-reference' in linters:
        result += find_linters_by('reference', linters['by-reference'])

    return list(set(result))
