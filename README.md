


### Usage


```python
from dictvalidator import

validator = dict_validator(
    name=string,
    secret="43",
    email=string,
    password=string,
    comment=optional(string),
    magic=either(45, "NOTHING"),
    random_value=optional,
)

validator({
    "name": "",
    "secret": "43",
    "email": "kdwqd@cool",
    "password": "kdwqd",
    "magic": "NOTHING",
    "random_value": False,
})
```
