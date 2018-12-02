"""
The model of the model.

Key concepts:

* A **model** is a custom class, e.g. `Course`, which can be serialized
  to/from JSON.

* A **converter** describes how to:

  - load something from a JSON-compatible dict
  - dump something to JSON-compatible dict
  - get JSON schema for something

  There are converters for integers, lists of integers, models,
  dicts of models, etc.

* A **registry** is a collection of converters. Additionally it provides
  high-level API for loading and dumping, and for getting a self-contained
  schema.

* A **field** is an attribute of a model, e.g. `Course.title`.
  Each field usually *has* a converter (but it is not a converter itself).
  The field handles attributes that are optional in JSON.
  (In Python, missing attributes should be set to None rather than missing.)

"""
import collections.abc
import datetime
import textwrap
import inspect

import jsonschema


class BaseConverter:
    """Converts to/from JSON-compatible values and provides JSON schema
    """
    init_args = ()
    schema_url = None
    definition_key = None

    @property
    def _naucse__converter(self):
        return self

    def load(self, data, **init_kwargs):
        """Convert a JSON-compatible data to a Python value.

        `init_kwargs` are extra values passed to `__init__`, if necessary.
        The Converter's `init_args` attribute specifies which init_kwargs
        are supported.

        The base implementation returns `data` unchanged.
        """
        return data

    def dump(self, value):
        """Convert a Python value to JSON-compatible data.
        """
        return value

    def get_schema(self, context):
        """Return JSON schema for the JSON-compatible data.

        Must be reimplemented in subclasses.
        """
        raise NotImplementedError()


class NoneConverter(BaseConverter):
    def get_schema(self, context):
        return {'type': 'null'}


class StringConverter(BaseConverter):
    def get_schema(self, context):
        return {'type': 'string'}


class BoolConverter(BaseConverter):
    def get_schema(self, context):
        return {'type': 'boolean'}


class IntegerConverter(BaseConverter):
    def load(self, data):
        return int(data)

    def get_schema(self, context):
        return {'type': 'integer'}


class FloatConverter(BaseConverter):
    def load(self, data):
        return float(data)

    def get_schema(self, context):
        return {'type': 'number'}


BUILTIN_CONVERTERS = {
    type(None): NoneConverter(),
    str: StringConverter(),
    bool: BoolConverter(),
    int: IntegerConverter(),
    float: FloatConverter(),
}

def get_converter(key):
    try:
        converter = key._naucse__converter
    except AttributeError as e:
        if type(key) in BUILTIN_CONVERTERS:
            return BUILTIN_CONVERTERS[type(key)]
        elif key in BUILTIN_CONVERTERS:
            return BUILTIN_CONVERTERS[key]
        raise TypeError(f'{key} is not a converter') from e
    return converter._naucse__converter


class ListConverter(BaseConverter):
    """Converts lists of convertable items

    `item_converter` is a Converter for individual items.

    If `index_arg` is given, the item index is passed to the `item_converter`'s
    `load` method under this name.
    """
    def __init__(self, item_converter, *, index_arg=None):
        self.item_converter = get_converter(item_converter)
        self.init_args = self.item_converter.init_args
        self.index_arg = index_arg

    def load(self, data, **init_kwargs):
        result = []
        for index, d in enumerate(data):
            if self.index_arg:
                init_kwargs[self.index_arg] = index
            result.append(self.item_converter.load(d, **init_kwargs))
        return result

    def dump(self, value):
        return [self.item_converter.dump(v) for v in value]

    def get_schema(self, context):
        return {
            'type': 'array',
            'items': context.get_schema(self.item_converter),
        }


class DictConverter(BaseConverter):
    """Converts dicts with string keys and values of convertable items

    `item_converter` is a Converter for the values.

    If `key_arg` is given, the key is passed to the `item_converter`'s
    `load` method under this name.
    """
    def __init__(self, item_converter, *, key_arg=None):
        self.item_converter = get_converter(item_converter)
        self.init_args = self.item_converter.init_args
        self.key_arg = key_arg

    def load(self, data, **init_kwargs):
        result = {}
        for k, v in data.items():
            if self.key_arg:
                init_kwargs[self.key_arg] = k
            result[k] = self.item_converter.load(v, **init_kwargs)
        return result

    def dump(self, value):
        return {k: self.item_converter.dump(v) for k, v in value.items()}

    def get_schema(self, context):
        return {
            'type': 'object',
            'additionalProperties': context.get_schema(self.item_converter),
        }


class KeyAttrDictConverter(BaseConverter):
    """Handle an ordered dict that's serialized as a list

    The key of the dict is an attribute of its corresponding value,
    named in `key_attr`.

    If `index_arg` is given, the item index is passed to the `item_converter`'s
    `load` method under this name.
    """
    def __init__(self, item_converter, *, key_attr, index_arg=None):
        self.item_converter = get_converter(item_converter)
        self.key_attr = key_attr
        self.index_arg = index_arg
        self.init_args = set(self.item_converter.init_args)

    def load(self, data, **init_kwargs):
        result = {}
        for index, value in enumerate(data):
            if self.index_arg:
                init_kwargs[self.index_arg] = index
            item = self.item_converter.load(value, **init_kwargs)
            result[getattr(item, self.key_attr)] = item
        return result

    def dump(self, value):
        return [self.item_converter.dump(v) for k, v in value.items()]

    def get_schema(self, context):
        return {
            'type': 'array',
            'items': context.get_schema(self.item_converter),
        }


def _classname(cls):
    return f'{cls.__module__}.{cls.__qualname__}'


class Field:
    """Descriptor for a Model's attribute that is loaded/dumped to JSON

    `converter`: Converter to use for the attribute.

    `name`: Name of the attribute (if None, set automatically when Field is
    used in a class).

    `data_key`: Key in the JSON mapping.

    `doc` is a documentation string. It appears as "description" of the JSON
    schema.

    `optional`: If True, `data_key` may be missing from the JSON mapping.
    Missing values are replaced by `None`, unless a `factory` is given or
    `default_factory` is added later.

    `factory` may be a zero-argument function used to produce default values.
    Assumes, `optional=True`.

    Additional customizations can be done using the `default_factory` and
    `after_load` decorators.

    If `input` is true, the attribute is loaded from JSON. If it's false,
    the default is always used (as set by `factory` or `default_factory`).

    If `output` is true, the attribute is dumped to JSON. If it is false,
    it will always be missing in the output.
    """
    def __init__(
        self, converter, *, name=None, data_key=None, doc=None,
        optional=False, factory=None,
        input=True, output=True,
    ):
        self.converter = get_converter(converter)
        self.name = name
        self.data_key = data_key or name
        self.optional = optional
        self.doc = doc
        self.input = input
        self.output = output

        self._after_load_hooks = []

        if factory:
            self.default_factory()(lambda i: factory())

    def __repr__(self):
        return f'<{_classname(type(self))} {self.name} ({self.converter})>'

    default = None

    def __set_name__(self, cls, name):
        self.name = name
        self.data_key = self.data_key or self.name

    def load_into(self, instance, data, **init_kwargs):
        if not self.input:
            value = self._load_missing(instance)
        else:
            init_kwargs = {
                n: v for n, v in init_kwargs.items()
                if n in self.converter.init_args
            }
            try:
                item_data = data[self.data_key]
            except KeyError:
                if self.optional:
                    value = self._load_missing(instance)
                else:
                    raise
            else:
                value = self.converter.load(item_data, **init_kwargs)
        setattr(instance, self.name, value)
        for func in self._after_load_hooks:
            func(instance)

    def _load_missing(self, instance):
        return None

    def dump_into(self, instance, data):
        if not self.output:
            return
        value = getattr(instance, self.name)
        if self.optional and value == self.default:
            return
        data[self.data_key] = self.converter.dump(value)

    def put_schema_into(self, object_schema, context):
        if context.is_input and not self.input:
            return
        if not context.is_input and not self.output:
            return
        schema = context.get_schema(self.converter)
        if self.doc:
            schema['description'] = self.doc
        # XXX: set schema['default'] ?
        object_schema['properties'][self.data_key] = schema
        if not self.optional:
            object_schema.setdefault('required', []).append(self.data_key)
        if not context.is_input:
            object_schema['additionalProperties'] = False

    def __get__(self, owner, instance, m=None):
        if instance is None:
            return self
        type_name = type(owner).__name__
        raise AttributeError(
            f'{self.name!r} of {type_name} object was not yet loaded'
        )

    def default_factory(self):
        """Decorate a function that will be called to produce a default value

        The decorated function will be called with the loaded instance
        as first argument.
        """
        def _decorator(func):
            self.optional = True
            self._load_missing = func
            return func
        return _decorator

    def after_load(self):
        """Decorate a function that will be called after an attribute is loaded

        The decorated function will be called with the loaded instance
        as first argument.
        """
        def _decorator(func):
            self._after_load_hooks.append(func)
            return func
        return _decorator


class ModelConverter(BaseConverter):
    def __init__(self, cls, *, slug=None, init_args=()):
        self.cls = cls
        self.name = cls.__name__
        self.doc = inspect.getdoc(cls)
        self.fields = {}
        self.init_args = init_args
        self.definition_key = slug

        for name, field in vars(cls).items():
            if name.startswith('__') or not isinstance(field, Field):
                continue
            self.fields[name] = field

    def __repr__(self):
        return f'<{_classname(type(self))} for {_classname(self.cls)}>'

    def load(self, data, **init_kwargs):
        result = self.cls(**init_kwargs)
        for field in self.fields.values():
            field.load_into(result, data, parent=result)
        return result

    def dump(self, value):
        result = {}
        for field in self.fields.values():
            field.dump_into(value, result)
        return result

    def get_schema(self, context):
        schema = {
            'type': 'object',
            'title': self.cls.__name__,
            'properties': {},
        }
        if self.doc:
            schema['description'] = self.doc
        for field in self.fields.values():
            field.put_schema_into(schema, context)
        return schema


class SchemaContext:
    def __init__(self, *, is_input):
        self.definition_refs = {}
        self.definitions = {}
        self.is_input = is_input

    def get_schema(self, converter):
        if converter.definition_key:
            if converter not in self.definition_refs:
                key = converter.definition_key
                if key in self.definitions:
                    raise ValueError(f'duplicate key {key}')
                self.definitions[key] = converter.get_schema(self)
                self.definition_refs[converter] = f'#/definitions/{key}'
            return {'#ref': self.definition_refs[converter]}
        return converter.get_schema(self)


def get_schema(converter, *, is_input):
    converter = get_converter(converter)
    context = SchemaContext(is_input=is_input)
    context.definitions.update({
        'ref': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                '$ref': {
                    'type': 'string',
                    'format': 'uri',
                },
            },
        },
        'api_version': {
            'type': 'array',
            'items': {'type': 'integer'},
            'minItems': 2,
            'maxItems': 2,
            'description': textwrap.dedent("""
                Version of the information, and of the schema,
                as two integers – [major, minor].
                The minor version is increased on every change to the
                schema that keeps backwards compatibility for forks
                (i.e. input data).
                The major version is increased on incompatible changes.
            """),
        },
    })
    ref = context.get_schema(converter)
    return {
        **ref,
        '$schema': 'http://json-schema.org/draft-06/schema#',
        'definitions': context.definitions,
    }


def dump(instance, converter=None):
    if converter is None:
        converter = get_converter(instance)
    converter = get_converter(converter)
    schema = get_schema(converter, is_input=False)
    result = converter.dump(instance)
    jsonschema.validate(result, schema)
    return result


def load(converter, data, **init_kwargs):
    converter = get_converter(converter)
    schema = get_schema(converter, is_input=True)
    jsonschema.validate(data, schema)
    return converter.load(data, **init_kwargs)


def register_model(cls, converter=None):
    if converter is None:
        converter = ModelConverter(cls)
    cls._naucse__converter = converter
    return cls
