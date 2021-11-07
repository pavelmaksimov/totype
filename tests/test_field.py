import pytest

from totype.fields import Field


def test_field():
    field = Field("name")

    value = "text"
    valid, new_value = field(value)

    assert valid
    assert new_value == value


def test_error_mod_ignore():
    value = "text"

    field = Field("name", transform_funcs=[int], errors="ignore")
    valid, new_value = field(value)

    assert not valid
    assert new_value == value


def test_error_mod_raise():
    value = "text"

    field = Field("name", transform_funcs=[int], errors="raise")

    with pytest.raises(ValueError):
        field(value)


def test_error_mod_default():
    value = "text"
    default_value = 0

    field = Field("name", transform_funcs=[int], errors="default", default_value=default_value)
    valid, new_value = field(value)

    assert not valid
    assert new_value == default_value


def test_transform_field():
    field = Field("name", transform_funcs=[int, lambda x: x * 100])

    value = "1"
    valid, new_value = field(value)

    assert valid
    assert new_value == 100


def test_default_value():
    default_value = "def"
    field = Field("name", transform_funcs=[int], default_value=default_value)

    value = "text"
    valid, new_value = field(value)

    assert not valid
    assert new_value == default_value


def test_clear_values():
    default_value = "def"
    value = "text"

    field = Field("name", transform_funcs=[int], default_value=default_value, clear_values={value})
    valid, new_value = field(value)

    assert not valid
    assert new_value == default_value


def test_map_replace_values():
    default_value = "def"
    value = "text"
    replace_value = value+value
    map_replace_values = {value: replace_value}

    field = Field("name", transform_funcs=[int], default_value=default_value, map_replace_values=map_replace_values)
    valid, new_value = field(value)

    assert not valid
    assert new_value == default_value
