from typing import Dict, Tuple, Callable, Optional
import os

from dictvalidator.validators import (
    string,
    integer,
    optional,
    _EitherHolder,
    _RegexHolder,
    either,
    format_validator,
    _is_optional_validator,
)


def _setup_colors() -> Tuple[Callable, bool]:
    """
    Colors can be disabled before running by setting the environment variable
    `DICTVALIDATOR_USE_COLORS=1` or during runtime with:

    >>> import dictvalidator
    >>> dictvalidator.use_colors = False
    ```
    """
    if os.getenv("DICTVALIDATOR_USE_COLORS", "0").lower() in ["1", "true"]:
        try:
            import termcolor
            return termcolor.colored, True
        except ModuleNotFoundError:
            pass

    def colored(*args, **kwargs):
        if args:
            return args[0]
        else:
            return ""
    return colored, False

colored, use_colors = _setup_colors()

class ValidationError(Exception):
    pass


def format_field(field_name: str) -> str:
    if use_colors:
        return colored(field_name, "cyan")
    else:
        return f'"{field_name}"'


def format_regex_pattern(pattern: str) -> str:
    if use_colors:
        return f"`{colored(pattern, 'cyan')}`"
    else:
        return f"`{pattern}`"


def _existence_pass(___value___mangled, *args, **kwargs) -> None:
    """
    The first argument is mangled as `___value___mangled` as opposed to
    `value` since otherwise it would prevent us from having a kwargs key called
    `value`
    """
    print("-- First pass: existence")
    for field_name, validator in kwargs.items():
        if field_name in ___value___mangled:
            print(f"Found field_name `{field_name}`")
        else:
            print(f"Did not find field_name `{field_name}`")
            if _is_optional_validator(validator):
                print("...but it was optional anyway")
                continue
            else:
                raise ValidationError(
                    f"Missing required field `{field_name}`")

def _expect_bool(field_name, value) -> None:
    if not isinstance(value, bool):
        raise ValidationError(
            f"Expected field `{field_name}` to be a boolean,"
            f" was {type(value)}")


def _expect_instance(
        field_name, value, instance, instance_name: Optional[str]=None) -> None:
    if not isinstance(value, instance):
        raise ValidationError(
            f"Expected field `{field_name}` to be"
            f" {instance_name or instance},"
            f" was {type(value)}")


def _expect_string(field_name, value) -> None:
    if not isinstance(value, str):
        raise ValidationError(
            f"Expected field `{field_name}` to be a string,"
            f" was {type(value)}")


def _expect_integer(field_name, value) -> None:
    if not isinstance(value, int):
        raise ValidationError(
            f"Expected field `{field_name}` to be an integer,"
            f" was {type(value)}")


def _expect_value(field_name, found, expected) -> None:
    if found != expected:
        raise ValidationError(
            "Expected field `{}` to have value {}, found {}".format(
                field_name, expected, found))


def _expect_is(field_name, found, expected) -> None:
    if found is not expected:
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

    elif isinstance(validator, bool):
        # dict_validator(my_field=True)
        _expect_bool(field_name, value)
        _expect_is(field_name, found=value, expected=validator)

    elif isinstance(validator, str):
        # dict_validator(my_field="bar")
        _expect_string(field_name, value)
        _expect_value(field_name, found=value, expected=validator)

    elif isinstance(validator, int):
        # dict_validator(my_field=49)
        _expect_integer(field_name, value)
        _expect_value(field_name, found=value, expected=validator)

    elif validator is any:
        pass

    elif validator is bool:
        _expect_bool(field_name, value)

    elif validator is bytes or validator is list:
        _expect_instance(field_name, value, validator)

    elif validator is str or validator is string:
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

    elif isinstance(validator, _RegexHolder):
        _expect_string(field_name, value)

        match = validator.compiled_pattern.match(value)
        if not match:
            raise ValidationError(
                "Field {} did not match expected regex pattern {}".format(
                    format_field(field_name),
                    format_regex_pattern(validator.compiled_pattern.pattern)))

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
