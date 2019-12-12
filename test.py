from dictvalidator import dict_validator, string, optional, either


def test_0():
    print("\n" + "*"*10 + " Big test")
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
    print("\n" + "*"*10 + " Either test")
    validator = dict_validator(secret=either(string("9"), 0))
    validator({"secret": 0})


def test_either_failure():
    print("\n" + "*"*10 + " Either test (failing)")
    validator = dict_validator(secret=either("43", "44"))
    validator({"secret": "40"})


def main():
    test_0()
    test_either_success()


if __name__ == "__main__":
    main()
