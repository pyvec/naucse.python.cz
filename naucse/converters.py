"""
The model of the model.

Key concepts:

* A **model** is a custom class, e.g. `Course`, which can be serialized
  to/from JSON.

* A **converter** describes how to:

  - load something from a JSON-compatible dict
  - dump something to JSON-compatible dict
  - get JSON schema for something

  There are converters for integers, lists of integers, modeld, dicts of models,
  etc.

* A **registry** is a collection of converters.

* A **field** is an entry in a model, e.g. `Course.title`.
  Each field usually *has* a converter, but it is not a converter itself.
  The field handles attributes that are optional in JSON.
  (In Python, missing attributes should be set to None rather than missing.)

"""
import datetime
import contextlib
import contextvars

import textwrap

_parents_var = contextvars.ContextVar('_parents_var', default=None)
_index_var = contextvars.ContextVar('_index_var')

@contextlib.contextmanager
def model_load_context(model):
    parents = _parents_var.get()
    if _parents_var.get() is None:
        token = _parents_var.set([model])
        yield
        _parents_var.reset(token)
    else:
        parents.append(model)
        yield
        parents.pop()


def get_parent():
    parents = _parents_var.get()
    if not parents:
        raise ValueError('No model is being loaded')
    return parents[-1]


def indexed(iterable):
    token = _index_var.set(0)
    try:
        for i, item in enumerate(iterable):
            _index_var.set(i)
            yield item
    finally:
        _index_var.reset(token)


def get_index():
    try:
        return _index_var.get()
    except LookupError as e:
        raise ValueError('Not sequence is being loaded') from e


class _Nothing:
    """Missing value"""
    def __bool__(self):
        return False

NOTHING = _Nothing()


class IntegerConverter:
    def load(self, data):
        return data

    def dump(self, value):
        return value

    def get_schema(self):
        return {'type': 'integer'}


class StringConverter:
    def load(self, data):
        return data

    def dump(self, value):
        return value

    def get_schema(self):
        return {'type': 'string'}


class DateConverter:
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


class ListConverter:
    def __init__(self, item_converter):
        self.item_converter = item_converter

    def load(self, data):
        return [self.item_converter.load(d) for d in indexed(data)]

    def dump(self, value):
        return [self.item_converter.dump(v) for v in value]

    def get_schema(self):
        return {
            'type': 'array',
            'items': self.item_converter.get_schema(),
        }


class DictConverter:
    """Handle a dict with string keys and values loaded by `item_converter`"""
    def __init__(self, item_converter):
        self.item_converter = item_converter

    def load(self, data):
        return {
            k: self.item_converter.load(v) for k, v in indexed(data.items())
        }

    def dump(self, value):
        return {k: self.item_converter.dump(v) for k, v in value.items()}

    def get_schema(self):
        return {
            'type': 'object',
            'additionalProperties': self.item_converter.get_schema(),
        }


class KeyAttrDictConverter:
    """Handle an ordered dict that's serialized as a list

    The key of the dict is an attribute of its values, usually a `slug`.
    """
    def __init__(self, item_converter, *, key_attr):
        self.item_converter = item_converter
        self.key_attr = key_attr

    def load(self, data):
        result = {}
        for value in indexed(data):
            item = self.item_converter.load(value)
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
            self.constructor()(lambda i: factory())

    default = None

    def __set_name__(self, cls, name):
        self.name = name
        self.data_key = self.data_key or self.name

    def load_into(self, instance, data):
        if self.converter is None:
            value = self._load_missing(instance, data)
        else:
            try:
                item_data = data[self.data_key]
            except KeyError:
                if self.optional:
                    value = self._load_missing(instance, data)
                else:
                    raise
            else:
                value = self.converter.load(item_data)
        setattr(instance, self.name, value)
        for func in self._after_load_hooks:
            func(instance)

    def _load_missing(self, instance, data):
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

    def constructor(self):
        def _decorator(func):
            self.optional = True
            self._load_missing = lambda instance, data: func(instance)
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
        result.constructor()(func)
        return result
    return _decorator


class ModelConverter:
    def __init__(self, cls, *, doc=None):
        self.cls = cls
        self.name = cls.__name__
        self.fields = {}
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
        with model_load_context(result):
            for field in self.iter_fields():
                field.load_into(result, data)
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

    def register_model(self, cls):
        self._converters[cls] = ModelConverter(cls)
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
