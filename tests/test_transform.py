from totype import fields
from totype.transform import RowTransform
import datetime as dt


def test_RowTransform():
    transform = RowTransform(
        fields=[
            fields.TextField(),
            fields.IntField(),
            fields.UIntField(),
            fields.FloatField(),
            fields.DateTimeField(),
            fields.DateField(),
            fields.ArrayField(),
            fields.JSONField(),
        ],
        skip_error_rows=False,
        store_rows_with_errors=False,
    )
    newrow = transform(
        (1, "20", "-100", "500", "2021-01-01", "2021-01-01", "[[100]]", '{"100": 100}')
    )
    assert newrow == ("1", 20, 0, 500.0, dt.datetime(2021,1,1), dt.date(2021,1,1), [[100]], {"100": 100})
    assert not transform._rows_with_errors


def test_RowTransform_skip_error_rows():
    transform = RowTransform(
        fields=[
            fields.TextField("name"),
            fields.IntField("name"),
        ],
        skip_error_rows=True,
        store_rows_with_errors=False,
    )
    assert transform((100, )) == ('100',)
    assert transform((100, "200", 0)) == ('100', 200)
    assert not transform._rows_with_errors


def test_RowTransform_store_rows_with_errors():
    transform = RowTransform(
        fields=[
            fields.TextField("name"),
            fields.IntField("name"),
        ],
        skip_error_rows=True,
        store_rows_with_errors=True,
    )
    row_with_error1 = ('100',)
    row_with_error2 = (100, "200", 0)

    transform(row_with_error1)
    transform((100, "200"))
    transform(row_with_error2)

    assert transform._rows_with_errors == {0: row_with_error1, 2: row_with_error2}


def test_RowTransform_as_namedtuple():
    transform = RowTransform(
        fields=[
            fields.TextField("Text"),
            fields.IntField("Integer"),
        ],
        skip_error_rows=True,
        store_rows_with_errors=True,
    )

    result = transform.as_namedtuple(
        transform((100, "200"))
    )

    assert result.Text == "100"
    assert result.Integer == 200
