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
import datetime

import textwrap


class BaseConverter:
    """Converts to/from JSON-compatible values and provides JSON schema
    """
    init_args = ()

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

    def get_schema(self):
        """Return JSON schema for the JSON-compatible data.

        Must be reimplemented in subclasses.
        """
        raise NotImplementedError()


class IntegerConverter(BaseConverter):
    def get_schema(self):
        return {'type': 'integer'}


class StringConverter(BaseConverter):
    def get_schema(self):
        return {'type': 'string'}


class DateConverter(BaseConverter):
    """Converts datetime.datetime values to 'YYYY-MM-DD' strings."""
    def load(self, data):
        return datetime.datetime.strptime(data, "%Y-%m-%d").date()

    def dump(self, value):
        return str(value)

    def get_schema(self):
        return {
            'type': 'string',
            'pattern': r'[0-9]{4}-[0-9]{2}-[0-9]{2}',
            'format': 'date',
        }


class ListConverter(BaseConverter):
    """Converts lists of convertable items

    `item_converter` is a Converter for individual items.

    If `index_arg` is given, the item index passed to the `item_converter`'s
    `load` method under this name.
    """
    def __init__(self, item_converter, *, index_arg=None):
        self.item_converter = item_converter
        self.init_args = item_converter.init_args
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

    def get_schema(self):
        return {
            'type': 'array',
            'items': self.item_converter.get_schema(),
        }


class DictConverter(BaseConverter):
    """Converts dicts with string keys and values of convertable items

    `item_converter` is a Converter for the values.
    """
    def __init__(self, item_converter, *, key_arg=None):
        self.item_converter = item_converter
        self.init_args = item_converter.init_args
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

    def get_schema(self):
        return {
            'type': 'object',
            'additionalProperties': self.item_converter.get_schema(),
        }


class KeyAttrDictConverter(BaseConverter):
    """Handle an ordered dict that's serialized as a list

    The key of the dict is an attribute of its values, usually a `slug`.
    """
    def __init__(self, item_converter, *, key_attr, index_arg=None):
        self.item_converter = item_converter
        self.key_attr = key_attr
        self.index_arg = index_arg
        self.init_args = set(item_converter.init_args) | {index_arg}

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

    def get_schema(self):
        return {
            'type': 'array',
            'items': self.item_converter.get_schema(),
        }


class Field:
    def __init__(
        self, converter, *,
        name=None, data_key=None, optional=False, doc=None,
        factory=None,
    ):
        self.converter = converter
        self.name = name
        self.data_key = data_key or name
        self.optional = optional
        self.doc = doc

        self._after_load_hooks = []

        if factory:
            self.default_factory()(lambda i: factory())

    default = None

    def __set_name__(self, cls, name):
        self.name = name
        self.data_key = self.data_key or self.name

    def load_into(self, instance, data, **init_kwargs):
        if self.converter is None:
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
        if self.converter is None:
            return
        value = getattr(instance, self.name)
        if self.optional and value == self.default:
            return
        data[self.data_key] = value

    def put_schema_into(self, object_schema):
        if self.converter is None:
            return
        schema = self.converter.get_schema()
        if self.doc:
            schema['description'] = self.doc
        # XXX: set schema['default'] ?
        object_schema['properties'][self.data_key] = schema
        if not self.optional:
            object_schema.setdefault('required', []).append(self.data_key)

    def __get__(self, owner, instance, m=None):
        if instance is None:
            return self
        type_name = type(owner).__name__
        raise AttributeError(
            f'{self.name!r} of {type_name} object was not yet loaded'
        )

    def default_factory(self):
        def _decorator(func):
            self.optional = True
            self._load_missing = func
            return func
        return _decorator

    def after_load(self):
        def _decorator(func):
            self._after_load_hooks.append(func)
            return func
        return _decorator


def loader():
    def _decorator(func):
        result = Field(None, data_key=None)
        result.default_factory()(func)
        return result
    return _decorator


class ModelConverter(BaseConverter):
    def __init__(self, cls, *, init_args=(), doc=None):
        self.cls = cls
        self.name = cls.__name__
        self.fields = {}
        self.init_args = init_args
        for name, field in vars(cls).items():
            if name.startswith('__') or not isinstance(field, Field):
                continue
            self.fields[name] = field

        if doc is None:
            doc = cls.__doc__
        self.doc = doc

    def iter_fields(self):
        for name, field in vars(self.cls).items():
            if name.startswith('__') or not isinstance(field, Field):
                continue
            yield field

    def load(self, data, **init_kwargs):
        result = self.cls(**init_kwargs)
        for field in self.iter_fields():
            field.load_into(result, data, parent=result)
        return result

    def dump(self, value):
        result = {}
        for field in self.iter_fields():
            field.dump_into(value, result)
        return result

    def get_schema(self):
        schema = {
            'type': 'object',
            'properties': {},
        }
        if self.doc:
            schema['description'] = self.doc
        for field in self.iter_fields():
            field.put_schema_into(schema)
        return schema


class Registry:
    def __init__(self, converters=None):
        if converters is None:
            converters = {
                int: IntegerConverter(),
                str: StringConverter(),
                datetime.date: DateConverter(),
            }
        self._converters = converters

    def register_model(self, cls, *, init_args=()):
        self._converters[cls] = ModelConverter(
            cls, init_args=init_args,
        )
        return cls

    def __getitem__(self, key):
        return self._converters.get(key, key)

    def load(self, key, data, **init_kwargs):
        converter = self[key]
        return converter.load(data, **init_kwargs)

    def dump(self, key, instance=None):
        if instance is None:
            instance = key
            key = type(key)
        converter = self[key]
        return converter.dump(instance)

    def get_schema(self, key):
        converter = self[key]
        definitions = {
            cls.__name__: model.get_schema()
            for cls, model in self._converters.items()
        }
        definitions.update({
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
        return {
            '$ref': f'#/definitions/{converter.name}',
            '$schema': 'http://json-schema.org/draft-06/schema#',
            'definitions': definitions,
        }
