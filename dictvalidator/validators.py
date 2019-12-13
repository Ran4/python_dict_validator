from typing import List, Tuple
import re

# Implicit: tuple of validators -> All tuple elements must validate correctly
# Implicit: [a, b, ...] -> Must fulfill all validators a, b, ...
# Implicit: True/False -> Must be True/False
# Implicit: "something" -> Equal to "something"
# Implicit: 34 -> Equal to 34
# Implicit: any (builtin) -> Field must exists, but may be of any type
# Implicit: bool (builtin) -> Must be True/False
# Implicit: bytes (builtin) -> Must be bytes instance
# Implicit: list (builtin) -> Must be a list instance
# Implicit: tuple (builtin) -> Must be a tuple instance
# Implicit: str (builtin) -> Must be a string

def string(expected):
    return (string, expected)


def integer(expected):
    return (integer, expected)


def optional(type_):
    return (optional, type_)


class _RegexHolder:
    def __init__(self, pattern: str):
        self.compiled_pattern = re.compile(pattern)


def regex(pattern):
    return _RegexHolder(pattern)


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
