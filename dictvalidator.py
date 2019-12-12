from typing import Dict, List, Tuple


class ValidationError(Exception):
    pass

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


def _existence_pass(value, *args, **kwargs) -> None:
    print("-- First pass: existence")
    for field_name, validator in kwargs.items():
        if field_name in value:
            print(f"Found field_name `{field_name}`")
        else:
            print(f"Did not find field_name `{field_name}`")
            if _is_optional_validator(validator):
                print("...but it was optional anyway")
                continue
            else:
                raise ValidationError(
                    f"Missing required field `{field_name}`")

def _expect_string(field_name, value) -> None:
    if not isinstance(value, str):
        raise ValidationError(
            f"Expected field `{field_name}` to be a string,"
            f" was {type(field_name)}")
    print(f"`{field_name}` was a string")


def _expect_integer(field_name, value) -> None:
    if not isinstance(value, int):
        raise ValidationError(
            f"Expected field `{field_name}` to be an integer,"
            f" was {type(field_name)}")
    print(f"`{field_name}` was an integer")


def _expect_value(field_name, found, expected) -> None:
    if found != expected:
        raise ValidationError(
            "Expected field `{}` to have value {}, found {}".format(
                field_name, expected, found))


def _validate_validator_tuple(field_name, value, validator: Tuple) -> None:
    assert isinstance(validator, tuple)
    for subvalidator in validator:
        print(f"Validating {format_validator(subvalidator)}")
        _validate(field_name, value, subvalidator)


def _validate(field_name: str, value, validator) -> None:
    print("--- Field {} should be {}".format(
        field_name, format_validator(validator),
    ))
    if isinstance(validator, tuple):
        _validate_validator_tuple(field_name, value, validator)

    elif isinstance(validator, str):
        # dict_validator(my_field="bar")
        _expect_string(field_name, value)
        _expect_value(field_name, found=value, expected=validator)

    elif isinstance(validator, int):
        # dict_validator(my_field=49)
        _expect_integer(field_name, value)
        _expect_value(field_name, found=value, expected=validator)

    elif validator is string:
        # my_field=string or my_field=string("foo")
        _expect_string(field_name, value)

        # my_field=string("foo"), where string("foo") == (string, "foo")
        if isinstance(validator, tuple):
            _validate_validator_tuple(field_name, value, validator)

    elif validator is integer:
        print("validator is integer")
        # my_field=integer or my_field=integer(48)
        _expect_integer(field_name, value)

        # my_field=integer("foo"), where integer("foo") == (integer, "foo")
        if isinstance(validator, tuple):
            _validate_validator_tuple(field_name, value, validator)

    elif validator is optional:
        # my_field=optional
        pass

    elif isinstance(validator, _EitherHolder):
        any_success = False
        for subvalidator in validator.validators:
            print(f"Applying sub-validator {format_validator(subvalidator)}")
            try:
                _validate(field_name, value, subvalidator)
                # At least one succeeded
                return
            except ValidationError:
                pass
        raise ValidationError(
            "Field `{}` did not fullfill requirement {}".format(
                field_name, format_validator(validator)))

    else:
        raise Exception(f"Unknown validator {validator} on field `{field_name}`")


def _validation_pass(d, *args, **kwargs) -> None:
    print("\n-- Second pass: validation")
    for field_name, validator in kwargs.items():
        if field_name not in d:
            print(f"Skipping missing field `{field_name}`")
            continue

        value = d[field_name]
        _validate(field_name, value, validator)


def dict_validator(*args, **kwargs):
    def inner(value: Dict):
        if not isinstance(value, dict):
            raise ValidationError("Must be dict")

        _existence_pass(value, *args, **kwargs)
        _validation_pass(value, *args, **kwargs)
    return inner
