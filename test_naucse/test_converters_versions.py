import pytest
from jsonschema.exceptions import ValidationError

from naucse.converters import Field, VersionField, load, dump, get_schema
from naucse.converters import register_model, get_converter


class TestModel:
    versioned_field = VersionField({
        # (Versions are out of order to test that VersionField sorts them)
        (0, 1): Field(str, optional=True, doc='Introducing new field'),
        (1, 0): Field(int, optional=True, doc="Let's make it an int"),
        (0, 5): Field(bool, optional=True, doc="Actually it's a bool"),
        (2, 0): Field(int, doc='No longer optional'),
    })

register_model(TestModel)
get_converter(TestModel).get_schema_url = lambda *a, **ka: ""

TEST_DATA = {
    (0, 1): "a",
    (0, 2): "b",
    (0, 5): True,
    (0, 6): False,
    (1, 0): 123,
    (2, 1): 456,
}


@pytest.mark.parametrize(
    'version',
    ((0, 0), (0, 1), (0, 2), (0, 5), (0, 6), (1, 0)),
)
def test_load_nothing(version):
    result = load(TestModel, {
        'api_version': list(version),
        'data': {},
    })
    assert result.versioned_field == None


def test_not_optional():
    with pytest.raises(ValidationError):
        load(TestModel, {
            'api_version': [2, 0],
            'data': {},
        })


@pytest.mark.parametrize(('version', 'data'), TEST_DATA.items())
def test_load_data(version, data):
    result = load(TestModel, {
        'api_version': list(version),
        'data': {'versioned_field': data},
    })
    assert result.versioned_field == data


@pytest.mark.parametrize(
    ('version', 'data'),
    (
        ((0, 0), 123),
        ((0, 0), "ab"),
        ((0, 1), True),
        ((1, 0), "ab"),
        ((1, 1), "ab"),
    ),
)
def test_load_wrong_data(version, data):
    with pytest.raises(ValidationError):
        result = load(TestModel, {
            'api_version': (0, 0),
            'data': {'versioned_field': 123},
        })


@pytest.mark.parametrize(('version', 'data'), TEST_DATA.items())
def test_dump_data(version, data):
    data_dict = {
        'api_version': list(version),
        'data': {'versioned_field': data},
    }
    result = load(TestModel, data_dict)
    assert dump(result, version=version) == {'$schema': '', **data_dict}


@pytest.mark.parametrize(('version', 'data'), TEST_DATA.items())
def test_dump_v0(version, data):
    data_dict = {
        'api_version': list(version),
        'data': {'versioned_field': data},
    }
    result = load(TestModel, data_dict)
    assert dump(result, version=(0, 0)) == {
        '$schema': '',
        'api_version': [0, 0],
        'data': {},
    }


@pytest.mark.parametrize(
    ('version', 'expected'),
    {
        (0, 0): None,
        (0, 1): "Introducing new field\n\nAdded in API version 0.1",
        (0, 2): "Introducing new field\n\nAdded in API version 0.1",
        (0, 5): "Actually it's a bool\n\nModified in API version 0.5",
        (1, 0): "Let's make it an int\n\nModified in API version 1.0",
        (1, 1): "Let's make it an int\n\nModified in API version 1.0",
        (2, 1): 'No longer optional\n\nModified in API version 2.0',
    }.items()
)
def test_doc(version, expected):
    schema = get_schema(TestModel, is_input=True, version=version)
    print(schema)
    properties = schema['properties']['data']['properties']
    if expected == None:
        assert 'versioned_field' not in properties
    else:
        doc = properties['versioned_field']['description']
        assert doc == expected
