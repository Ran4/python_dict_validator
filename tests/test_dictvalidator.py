import pytest

from dictvalidator import dict_validator, ValidationError
import dictvalidator.validators as v


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


def test_str():
    validator = dict_validator(name=str)
    validator({"name": "hello"})


def test_str_failure():
    validator = dict_validator(name=str)
    with pytest.raises(ValidationError):
        validator({"name": 40})


def test_string():
    validator = dict_validator(name=v.string)
    validator({"name": "hello"})


def test_string_failure():
    validator = dict_validator(name=v.string)
    with pytest.raises(ValidationError):
        validator({"name": 40})


def test_bytes():
    validator = dict_validator(value=bytes)
    validator({"value": b"hello world"})


def test_bytes_failure():
    validator = dict_validator(value=bytes)
    with pytest.raises(ValidationError):
        validator({"value": "hello world"})


def test_list():
    validator = dict_validator(value=list)
    validator({"value": []})


def test_list_failure():
    validator = dict_validator(value=list)
    with pytest.raises(ValidationError):
        validator({"value": (0,)})


def test_tuple():
    validator = dict_validator(value=tuple)
    validator({"value": (3, 4)})


def test_tuple_failure():
    validator = dict_validator(value=tuple)
    with pytest.raises(ValidationError):
        validator({"value": [1, 2]})


def test_either():
    validator = dict_validator(secret=v.either(v.string("9"), 0))
    validator({"secret": 0})


def test_either_failure():
    validator = dict_validator(secret=v.either("43", "44"))
    with pytest.raises(ValidationError):
        validator({"secret": "40"})


def test_regex():
    validator = dict_validator(value=v.regex(r".+ .+"))
    validator({"value": "hello world"})


def test_regex_failure():
    validator = dict_validator(value=v.regex(r".+ .+"))
    with pytest.raises(ValidationError):
        validator({"value": "helloworld"})


def test_bool_with_value_true():
    validator = dict_validator(value=bool)
    validator({"value": True})


def test_bool_with_value_false():
    validator = dict_validator(value=bool)
    validator({"value": False})


def test_bool_with_value_1_failure():
    validator = dict_validator(value=bool)
    with pytest.raises(ValidationError):
        validator({"value": 1})


def test_bool_with_value_0_failure():
    validator = dict_validator(value=bool)
    with pytest.raises(ValidationError):
        validator({"value": 0})


def test_true_with_value_true():
    validator = dict_validator(value=True)
    validator({"value": True})


def test_false_with_value_false():
    validator = dict_validator(value=False)
    validator({"value": False})


def test_true_with_value_1_failure():
    validator = dict_validator(value=True)
    with pytest.raises(ValidationError):
        validator({"value": 1})


def test_true_with_value_3_failure():
    validator = dict_validator(value=True)
    with pytest.raises(ValidationError):
        validator({"value": 3})


def test_false_with_value_0_failure():
    validator = dict_validator(value=False)
    with pytest.raises(ValidationError):
        validator({"value": 0})


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


def test_very_deep():
    validator = dict_validator(
        first_level=dict_validator(
            second_level=dict_validator(
                third_level=dict_validator(
                    fourth_level="ok",
                ),
            ),
        ))

    validator(dict(
        first_level=dict(
            second_level=dict(
                third_level=dict(
                    fourth_level="ok")))))

    with pytest.raises(ValidationError):
        validator(dict(
            first_level=dict(
                second_level=dict(
                    third_level=dict(
                        fourth_level="not ok")))))
