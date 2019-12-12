import pytest

from dictvalidator import (
    dict_validator,
    string,
    optional,
    either,
    ValidationError,
)


def test_0():
    validator = dict_validator(
        name=string,
        secret="43",
        email=string,
        password=string,
        comment=optional(string),
        random_value=optional,
    )

    validator({
        "name": "",
        "secret": "43",
        "email": "kdwqd@cool",
        "password": "kdwqd",
        #~ "comment": None,
        "random_value": False,
    })


def test_either_success():
    validator = dict_validator(secret=either(string("9"), 0))
    validator({"secret": 0})


def test_either_failure():
    validator = dict_validator(secret=either("43", "44"))
    with pytest.raises(ValidationError):
        validator({"secret": "40"})
