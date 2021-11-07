from totype import fields
import datetime as dt

from totype.func import _get_tz


def test_tz_datetime_datatype():
    transform = fields.DateTimeField("name", tz_name="Europe/Moscow")
    valid, new_value = transform("2021-01-01")

    assert valid
    assert isinstance(new_value, dt.datetime)
    assert new_value.tzinfo == _get_tz("Europe/Moscow")
    assert new_value == dt.datetime(2021, 1, 1, tzinfo=_get_tz("Europe/Moscow"))


def test_fmt_datetime_datatype():
    transform = fields.DateTimeField("name", fmt="%Y")
    valid, new_value = transform("2021")

    assert valid
    assert isinstance(new_value, dt.datetime)
    assert new_value == dt.datetime(2021, 1, 1)


def test_none_datetime_datatype():
    transform = fields.DateTimeField("name")
    valid, new_value = transform("None")

    assert valid
    assert isinstance(new_value, dt.datetime)
    assert new_value == dt.datetime(1970, 1, 1)


def test_novalid_datetime_datatype():
    transform = fields.DateTimeField("name")
    valid, new_value = transform("0")

    assert not valid
    assert isinstance(new_value, dt.datetime)
    assert new_value == dt.datetime(1970, 1, 1)


def test_int():
    transform = fields.IntField("name")
    valid, new_value = transform("2021")

    assert valid
    assert new_value == 2021


def test_novalid_int():
    transform = fields.IntField("name")
    valid, new_value = transform("+")

    assert not valid
    assert new_value == 0


def test_uint():
    transform = fields.UIntField("name")
    valid, new_value = transform("2021")

    assert valid
    assert new_value == 2021


def test_novalid_uint():
    transform = fields.UIntField("name")
    valid, new_value = transform("-1")

    assert not valid
    assert new_value == 0


def test_float():
    transform = fields.FloatField("name")
    valid, new_value = transform("2021")

    assert valid
    assert new_value == 2021.0


def test_novalid_float():
    transform = fields.UIntField("name")
    valid, new_value = transform("x")

    assert not valid
    assert new_value == 0


def test_string():
    transform = fields.TextField("name")
    valid, new_value = transform(True)

    assert valid
    assert new_value == "True"


def test_tz_timestamp_datatype():
    transform = fields.TimestampField(
        "name", tz_name="Europe/Moscow", errors="raise"
    )
    valid, new_value = transform("0.0")

    assert valid
    assert isinstance(new_value, dt.datetime)
    assert new_value.tzinfo == _get_tz("Europe/Moscow")
    assert new_value == dt.datetime(1970, 1, 1, tzinfo=_get_tz("Europe/Moscow"))


def test_none_timestamp_datatype():
    transform = fields.TimestampField("name")
    valid, new_value = transform("None")

    assert valid
    assert isinstance(new_value, dt.datetime)
    assert new_value == dt.datetime(1970, 1, 1)


def test_array_datatype_from_list():
    transform = fields.ArrayField("name")
    valid, new_value = transform([["1"], [[2]]])

    assert valid
    assert new_value == [["1"], [[2]]]


def test_array_datatype_from_text():
    transform = fields.ArrayField("name")
    valid, new_value = transform('[["1"], [[2]]]')

    assert valid
    assert new_value == [["1"], [[2]]]


def test_array_datatype_depth1():
    transform = fields.ArrayField(
        "name", depth=1, transform_funcs_for_array_values=[str]
    )
    valid, new_value = transform('[["1"], [[2]]]')

    assert valid
    assert new_value == [str(["1"]), str([[2]])]


def test_array_datatype_depth2():
    transform = fields.ArrayField(
        "name", depth=2, transform_funcs_for_array_values=[str]
    )
    valid, new_value = transform('[["1"], [[2]]]')

    assert valid
    assert new_value == [["1"], [str([2])]]


def test_array_datatype_depth3():
    transform = fields.ArrayField(
        "name", depth=3, transform_funcs_for_array_values=[str]
    )
    valid, new_value = transform('[["1"], [[2]]]')

    assert valid
    assert new_value == [[[]], [[str(2)]]]


def test_json_datatype():
    transform = fields.JSONField("name")
    valid, new_value = transform('{"1": 1}')

    assert valid
    assert new_value == {"1": 1}
