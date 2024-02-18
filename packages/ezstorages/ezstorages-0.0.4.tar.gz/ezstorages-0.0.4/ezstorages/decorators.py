from dataclasses import dataclass
from inspect import Signature, Parameter
from typing import get_type_hints


def useTable(table_name) -> dataclass:
    def decorator(cls):
        cls.__tablename__ = table_name
        return dataclass(cls)
    return decorator

def typed_dataclass(cls):
    # Get type hints for the class
    hints = get_type_hints(cls)

    # Create constructor parameters based on type hints
    parameters = [
        Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, annotation=annotation)
        for name, annotation in hints.items()
    ]

    # Create a new constructor with the specified parameters
    def __init__(self, *args, **kwargs):
        for name, value in zip(hints, args):
            setattr(self, name, value)
        for name, value in kwargs.items():
            if name in hints:
                setattr(self, name, value)

    # Update the class dictionary
    cls.__init__ = __init__
    cls.__signature__ = Signature(parameters)
    return cls