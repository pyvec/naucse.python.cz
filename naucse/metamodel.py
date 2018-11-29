"""
The model of the model.

Key concepts:

* a **loader** describes how to:
  - load something from JSON
  - dump something to JSON
  - get JSON schema for something

"""
import datetime
import contextvars
import contextlib

import textwrap

current_schema = contextvars.ContextVar('current_schema')

@contextlib.contextmanager
def context(var, value):
    token = var.set(value)
    yield
    var.reset(token)


class _Nothing:
    """Missing value"""
    def __bool__(self):
        return False

NOTHING = _Nothing()

_standard_loaders = []
def loader(key):
    def _decorator(item):
        _standard_loaders.append((key, item()))
        return item
    return _decorator


def loader_for(key):
    schema = current_schema.get()
    return schema.get_loader(key)


@loader(int)
class Int:
    def __init__(self, *, min=None, max=None):
        self.schema = {'type': 'integer'}
        if min:
            self.schema['minimum'] = min
        if max:
            self.schema['maximum'] = max

    def load(self, data):
        return data

    def dump(self, value):
        return value

    def get_schema(self):
        return self.schema


@loader(str)
class String:
    def load(self, data):
        return data

    def dump(self, value):
        return value

    def get_schema(self):
        return {'type': 'string'}


@loader(datetime.date)
class Date:
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


class List:
    def __init__(self, item_key):
        self.item_key = item_key

    def load(self, data):
        return [self.item_model.load(d) for d in data]

    def dump(self, value):
        return [self.item_model.dump(v) for v in value]

    def get_schema(self):
        return {
            'type': 'array',
            'items': self.item_model.get_schema(),
        }


class Dict:
    def __init__(self, item_key):
        self.item_key = item_key

    def load(self, data):
        return {k: self.item_key.load(v) for k, v in data.items()}

    def dump(self, value):
        return {k: self.item_key.dump(v) for k, v in value.items()}

    def get_schema(self):
        return {
            'type': 'object',
            'additionalProperties': self.item_key.get_schema(),
        }


class KeyAttrDict:
    def __init__(self, item_key, *, key_attr):
        self.item_key = item_key
        self.key_attr = key_attr

    def load(self, data):
        result = {}
        for value in data:
            item = loader_for(self.item_key).load(value)
            result[getattr(item, self.key_attr)] = item
        return result

    def dump(self, value):
        return [self.item_key.dump(v) for k, v in value.items()]

    def get_schema(self):
        return {
            'type': 'array',
            'items': loader_for(self.item_key).get_schema(),
        }


class Field:
    def __init__(
        self, item_key, *,
        name=None, data_key=None,
        optional=False, default=NOTHING, factory=None, construct=None,
        convert=None,
        doc=None,
    ):
        self.item_key = item_key
        self.name = name
        self.data_key = data_key or name
        self.optional = optional
        self.default = self.schema_default = default
        self.factory = factory
        self.construct = construct
        self.convert = convert
        self.doc = doc
        self.post_loaders = []

        if self.optional and self.default is NOTHING:
            self.default = None

    def __set_name__(self, cls, name):
        self.name = name
        self.data_key = self.data_key or self.name

    def load_into(self, instance, data):
        try:
            item_data = data[self.data_key]
        except KeyError:
            if self.construct is not None:
                value = self.construct(instance, data)
            elif self.factory is not None:
                value = self.factory()
            elif self.default is not NOTHING:
                value = self.default
            else:
                raise
        else:
            value = loader_for(self.item_key).load(item_data)
        setattr(instance, self.name, value)
        for loader in self.post_loaders:
            loader(instance)

    def dump_into(self, instance, data):
        value = getattr(instance, self.name)
        if self.optional and value == self.default:
            return
        data[self.data_key] = value

    def put_schema_into(self, object_schema):
        schema = loader_for(self.item_key).get_schema()
        if self.doc:
            schema['description'] = self.doc
        if self.schema_default is not NOTHING:
            schema['default'] = self.default
        object_schema['properties'][self.data_key] = schema
        if not self.optional:
            object_schema.setdefault('required', []).append(self.data_key)

    def __get__(self, owner, instance, m=None):
        if instance is None:
            return self
        raise AttributeError(self.name)

    def constructor(self):
        def _decorator(func):
            self.construct = func
            self.optional = True
            return func
        return _decorator

    def post_loader(self):
        def _decorator(func):
            self.post_loaders.append(func)
            return func
        return _decorator


class Object:
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

    def load(self, data, **init_kwargs):
        result = self.cls(**init_kwargs)
        for name, field in self.fields.items():
            field.load_into(result, data)
        return result

    def dump(self, value):
        result = {}
        for name, field in self.fields.items():
            field.dump_into(value, result)
        return result

    def get_schema(self):
        schema = {
            'type': 'object',
            'properties': {},
        }
        if self.doc:
            schema['description'] = self.doc
        for name, field in self.fields.items():
            field.put_schema_into(schema)
        return schema


class Schema:
    def __init__(self):
        self._loaders = dict(_standard_loaders)

    def model(self):
        def _decorator(cls):
            self._loaders[cls] = Object(cls)
            return cls
        return _decorator

    def get_loader(self, key):
        return self._loaders.get(key, key)

    def load(self, key, data, **init_kwargs):
        loader = self.get_loader(key)
        with context(current_schema, self):
            return loader.load(data, **init_kwargs)

    def dump(self, key, instance=None):
        if instance is None:
            instance = key
            key = type(key)
        loader = self.get_loader(key)
        with context(current_schema, self):
            return loader.dump(instance)

    def get_schema(self, key, internal=False):
        if internal:
            # XXX
            return {}
        loader = self.get_loader(key)
        with context(current_schema, self):
            definitions = {
                cls.__name__: model.get_schema()
                for cls, model in self._loaders.items()
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
                '$ref': f'#/definitions/{loader.name}',
                '$schema': 'http://json-schema.org/draft-06/schema#',
                'definitions': definitions,
            }


_standard_loaders = tuple(_standard_loaders)
