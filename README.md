# Data converter


## Install
    poetry add totype

or

    pip install totype

## Examples

### Transform value

```python
from totype.fields import Field

value = "1"

field = Field(
    transform_funcs=[
        int, 
        lambda x: x * 100,
        str
    ]
)
valid, new_value = field(value)

assert valid
assert new_value == "100"


# Default value

value = ".1"

field = Field(
    transform_funcs=[int],
    default_value=0,
)
valid, new_value = field(value)

assert not valid
assert new_value == 0
```


### Transform rows
```python
import datetime as dt
from totype import fields, RowTransform


transform = RowTransform(
    fields=[
        fields.TextField(),
        fields.IntField(),
        fields.UIntField(),
        fields.FloatField(),
        fields.ArrayField(),
        fields.JSONField(),
        fields.DateTimeField(),
        fields.DateField(),
    ],
    skip_error_rows=False,
    store_rows_with_errors=False,
)
newrow = transform(
    (1, "20", "-100", "500", "[[100]]", '{"100": 100}', "2021-01-01", "2021-01-01")
)
assert newrow == ("1", 20, 0, 500.0, [[100]], {"100": 100}, dt.datetime(2021,1,1), dt.date(2021,1,1))
```