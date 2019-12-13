### Installation

```
git clone https://github.com/Ran4/python_dict_validator
pip install -e python_dict_validator
```

### Usage


```python
from dictvalidator import dict_validator
import dictvalidator.validators as v

validator = dict_validator(
    secret="43",
    name=dict_validator(
        first_name=v.string,
        surname=v.optional(v.string),
    ),
    email=v.string,
    password=v.string,
    comment=v.optional(v.string),
    magic=v.either(45, "NOTHING"),
    random_value=v.optional,
)
# `validator` is now of type `Callable[[Dict], None]`

# If this would fail, `dictvalidator.ValidationError` would be raised
validator({
    "secret": "43",
    "name": {
        "first_name": "",
        "surname": optional(string),
    },
    "email": "kdwqd@cool",
    "password": "kdwqd",
    "magic": "NOTHING",
    "random_value": False,
})
```

### Coloring

Colors in the output is disabled by default, but can be enabled by setting the environment variable
`DICTVALIDATOR_USE_COLORS=1`

### Running tests

* Activate a virtualenv
* `pip install -r requirements.txt`
* `pip install -e .`

then:

```bash
pytest -v
```
