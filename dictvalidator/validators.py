from typing import List, Tuple

# Implicit: "something" -> checks for equal to "something"
# Implicit: 34 -> checks for equal to 34

def string(expected):
    return (string, expected)


def integer(expected):
    return (integer, expected)


def optional(type_):
    return (optional, type_)


class _EitherHolder:
    def __init__(self, validators: List):
        self.validators = validators


def either(*validators):
    return _EitherHolder(validators)


def format_validator(validator) -> str:
    if isinstance(validator, tuple):
        return ", ".join(format_validator(v) for v in validator)
    elif validator is string:
        return "string"
    elif validator is integer:
        return "integer"
    elif validator is optional:
        return "optional"
    elif isinstance(validator, str):
        return f"equal to \"{validator}\""
    elif isinstance(validator, int):
        return f"equal to {validator}"
    elif isinstance(validator, _EitherHolder):
        return "one of:\n" + "\n".join("| " + format_validator(v)
                                       for v in validator.validators)
    else:
        return str(validator)


def _is_optional_validator(validator) -> bool:
    if validator is optional:
        return True
    elif isinstance(validator, tuple) and any(x is optional for x in validator):
        return True
    else:
        return False