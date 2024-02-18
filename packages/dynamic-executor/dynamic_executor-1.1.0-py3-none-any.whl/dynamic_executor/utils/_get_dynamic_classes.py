from types import ModuleType
from typing import Dict

from ..classes.DynamicClassCreator import DynamicClassCreator


def _get_dynamic_classes(module: ModuleType) -> Dict[str, DynamicClassCreator]:
    """Collects all dynamic classes from a module.

    :param module: A module to collect classes from.
    :return: A dictionary of (variable name, dynamic_class instance) pairs.
    """
    return dict(
        (variable, getattr(module, variable))
        for variable in dir(module)
        if getattr(module, variable) in DynamicClassCreator.created_classes
    )
