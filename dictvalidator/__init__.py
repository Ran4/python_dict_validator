from typing import Dict, Tuple

from dictvalidator.validators import (
    string,
    integer,
    optional,
    _EitherHolder,
    either,
    format_validator,
    _is_optional_validator,
)


class ValidationError(Exception):
    pass


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

    elif hasattr(validator, "__name__") and \
            validator.__name__ == "dict_validator_runner":
        validator(value)

    elif isinstance(validator, dict):
        return dict_validator(**validator)(value)

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
    """
    Usage:
    >>> validator = dict_validator(**validator_kwargs)
    OR
    >>> validator = dict_validator(validator_kwargs)
    >>> validator(some_dictionary)  # None or raises ValidationError
    where each element of `validator_kwargs` has a string key representing
    the field name and a value that must be a valid validation object.

    Examples, these are all identical:
    >>> dict_validator(secret=43)
    >>> dict_validator(secret=integer(43))
    >>> dict_validator({"secret": 43})
    """
    if not kwargs and args and isinstance(args[0], dict):
        return dict_validator(**args[0])

    def dict_validator_runner(value: Dict) -> None:
        """Validates input `value`.
        Returns:
            None - on success

        Raises:
            ValidationError - on validation error
        """
        if not isinstance(value, dict):
            raise ValidationError("Must be dict")

        _existence_pass(value, *args, **kwargs)
        _validation_pass(value, *args, **kwargs)
    return dict_validator_runner