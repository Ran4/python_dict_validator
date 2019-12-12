import pytest

from . import dict_validator, ValidationError
from . import validators as v


def test_0():
    validator = dict_validator(
        name=v.string,
        secret="43",
        email=v.string,
        password=v.string,
        comment=v.optional(v.string),
        random_value=v.optional,
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
    validator = dict_validator(secret=v.either(v.string("9"), 0))
    validator({"secret": 0})


def test_either_failure():
    validator = dict_validator(secret=v.either("43", "44"))
    with pytest.raises(ValidationError):
        validator({"secret": "40"})


def test_dict_syntax():
    validator = dict_validator({"secret": 43})
    validator({"secret": 43})


def test_dict_syntax2():
    validator = dict_validator({"secret": v.integer(v.either(43, 45))})
    validator({"secret": 43})

def test_deeper_with_dict_syntax():
    validator = dict_validator(
        first_level={
            "second_level": 43,
        })
    validator({"first_level": {"second_level": 43}})


def test_deeper_with_dict_validator_syntax():
    validator = dict_validator(
        first_level=dict_validator(
            second_level=43,
        ))
    validator({"first_level": {"second_level": 43}})
