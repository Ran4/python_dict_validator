### Installation

```
git clone https://github.com/Ran4/python_dict_validator
pip install -e python_dict_validator
```

### Usage


```python
from dictvalidator import dict_validator

validator = dict_validator(
    name=string,
    secret="43",
    email=string,
    password=string,
    comment=optional(string),
    magic=either(45, "NOTHING"),
    random_value=optional,
)
# `validator` is now of type `Callable[[Dict], None]`

# If this would fail, `dictvalidator.ValidationError` would be raised
validator({
    "name": "",
    "secret": "43",
    "email": "kdwqd@cool",
    "password": "kdwqd",
    "magic": "NOTHING",
    "random_value": False,
})
```


### Running tests

Activate a virtualenv, `pip install -r requirements.txt`, then:

```bash
pytest -v
```
