"""
The infrastructure behind naucse's data model.

Key concepts:

* A **model** is a custom class, e.g. `Course`, which can be serialized
  to/from JSON.
  Specific models are defined in models.py.

* A **converter** describes how to:

  - load something from a JSON-compatible dict
  - dump something to JSON-compatible dict
  - get JSON schema for something

  There are converters for integers, lists of integers, models,
  dicts of models, etc.

  One can get the "default" converter for many values (or types):
  - Basic JSONSchema scalars (None, bool, int, float, str) have hard-coded
    defaults
  - Other classes may register a converter using `register_model`,
    or manually setting the "_naucse__converter" property.
  Generic collections (list/dict) do *not* have a default converter, since
  their schema always depends on what's supposed to be inside.
  For them, the converter needs to be specified when loading/dumping.
  For other types, it might make sense to use a non-default converter, for
  example to restrict values (e.g. add minimum/maximum for integers).

* A **field** is an attribute of a model, e.g. `Course.title`.
  Each field usually *has* a converter (but it is not a converter itself).
  The field handles attributes that are optional in JSON.
  (In Python, missing attributes should be set to None rather than missing.)
  It also handles the description ("docstring").

The top-level functions `load`, `dump` and `get_schema` work on messages that
have the API version.
The input/output is automatically validated against the schema when
loading/dumping.
If some restriction on the data is represented in the schema, no additional
checks should be needed for it.
"""
import collections.abc
import datetime
import textwrap
import inspect

import jsonschema


class BaseConverter:
    """Converts to/from JSON-compatible values and provides JSON schema

    This class is designed to be subclassed. Subclasses may override:

    `load`, `dump`, `get_schema` (see docstrings)

    `load_arg_names`: Names of keyword arguments for the `load` method.
        Collection converters (for list & dict) pass these through.

    `get_schema_url`: A method that determines the schema URL for a given
        instance.
        If it returns None, values cannot be dumped using the top-level
        `dump` function.
        May also *be* None (which does the same as returning None).
        May be set on instances directly.

    `slug`: An identifier for schema definitions and for top-level messages.
        Should be None for simple converters, and converters that can be
        parametrized.
        If None, values cannot be dumped using the top-level `dump` function.
        Currently the slug must be unique across converters.
    """

    load_arg_names = ()
    get_schema_url = None
    slug = None

    @property
    def _naucse__converter(self):
        return self

    def load(self, data, context, **kwargs):
        """Convert a JSON-compatible data to a Python value.

        `context` is a `LoadContext`, which holds options (like the API
        version) for loading an entire tree of objects.

        `kwargs` are extra keyword arguments passed to `__init__`.
        The Converter's `load_arg_names` attribute specifies which kwargs
        are supported.

        The base implementation returns `data` unchanged.
        """
        return data

    def dump(self, value, context):
        """Convert a Python value to JSON-compatible data.

        `context` is a `DumpContext`, which holds options (like the API
        version) for dumping an entire tree of objects.

        The base implementation returns `value` unchanged.
        """
        return value

    def get_schema(self, context):
        """Return JSON schema for the JSON-compatible data.

        Must be reimplemented in subclasses.

        Getting the schema requires a context, which holds "global" definitions
        and options. See the `SchemaContext` class.
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
    def load(self, data, context):
        return int(data)

    def get_schema(self, context):
        return {'type': 'integer'}


class FloatConverter(BaseConverter):
    def load(self, data, context):
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

    If `index_arg` is given, the item's index is passed to the
    `item_converter`'s `load` method under this name.
    """
    def __init__(self, item_converter, *, index_arg=None):
        self.item_converter = get_converter(item_converter)
        self.load_arg_names = self.item_converter.load_arg_names
        self.index_arg = index_arg

    def load(self, data, context, **kwargs):
        result = []
        for index, d in enumerate(data):
            if self.index_arg:
                kwargs[self.index_arg] = index
            result.append(self.item_converter.load(d, context, **kwargs))
        return result

    def dump(self, value, context):
        return [self.item_converter.dump(v, context) for v in value]

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

    `required` are the keys the dict must contain (if any).
    """
    def __init__(self, item_converter, *, key_arg=None, required=()):
        self.item_converter = get_converter(item_converter)
        self.load_arg_names = self.item_converter.load_arg_names
        self.key_arg = key_arg
        self.required = required

    def load(self, data, context, **kwargs):
        result = {}
        for k, v in data.items():
            if self.key_arg:
                kwargs[self.key_arg] = k
            result[k] = self.item_converter.load(v, context, **kwargs)
        return result

    def dump(self, value, context):
        return {
            str(k): self.item_converter.dump(v, context)
            for k, v in value.items()
        }

    def get_schema(self, context):
        schema = {
            'type': 'object',
            'additionalProperties': context.get_schema(self.item_converter),
        }
        if self.required:
            schema['required'] = list(self.required)
        return schema


class KeyAttrDictConverter(BaseConverter):
    """Handle an ordered dict that's JSON-serialized as a list

    The key of the dict taken from an attribute of its corresponding value,
    named in `key_attr`.

    If `index_arg` is given, the item index is passed to the `item_converter`'s
    `load` method under this name.
    """
    def __init__(self, item_converter, *, key_attr, index_arg=None):
        self.item_converter = get_converter(item_converter)
        self.key_attr = key_attr
        self.index_arg = index_arg
        self.load_arg_names = set(self.item_converter.load_arg_names)

    def load(self, data, context, **kwargs):
        result = {}
        for index, value in enumerate(data):
            if self.index_arg:
                kwargs[self.index_arg] = index
            item = self.item_converter.load(value, context, **kwargs)
            result[getattr(item, self.key_attr)] = item
        return result

    def dump(self, value, context):
        return [self.item_converter.dump(v, context) for k, v in value.items()]

    def get_schema(self, context):
        return {
            'type': 'array',
            'items': context.get_schema(self.item_converter),
        }


def _classname(cls):
    return f'{cls.__module__}.{cls.__qualname__}'


class AbstractField:
    """Descriptor for a Model's attribute that is loaded/dumped to JSON

    See Field for the API.
    """

    def __get__(self, instance, owner):
        """Debug helper

        An initialized model instance should have values for all its fields
        in its __dict__.

        However, when loading, not all fields have been initialized yet.
        Attempts to get the value of such a field will raise an informative
        error, rather than return the Field object from the model class.
        """
        if instance is None:
            # Getting a class attribute -- return this Field
            return self
        else:
            # Getting an instnce attribute -- raise an error
            type_name = owner.__name__
            raise AttributeError(
                f'{self.name!r} of {type_name} object was not yet loaded'
            )

class Field(AbstractField):
    """Descriptor for a Model's attribute that is loaded/dumped to JSON

    `converter`: Converter to use for the attribute.

    `name`: Name of the attribute. (If None, set automatically when Field is
    used in a class.)

    `data_key`: Key in the JSON mapping. (Set to `name` by default.)

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

    Fields within a model are loaded (and dumped) in the order they appear
    in the model. Side-effects can take advantage of this.
    (Note: Additional functions such as `after_load` are called together with
    their field, regardless of where the function is defined.)
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

    def load_into(self, instance, data, context, **kwargs):
        """Load this field's data into the given Python object.

        `instance` is the Python object being initialized.

        `data` is the object's data loaded from JSON.
        (It may or might not contain a value for the field.)

        `kwargs` are passed to the converter's `load` (if called)

        This always sets the field's attribute on `instance`, if it succeeds.
        """
        if not self.input:
            # Ignore the input data entirely
            value = self._get_default(instance)
        else:
            try:
                item_data = data[self.data_key]
            except KeyError:
                # Get the default (if we can)
                if self.optional:
                    value = self._get_default(instance)
                else:
                    raise
            else:
                # Load data from JSON
                kwargs = {
                    n: v for n, v in kwargs.items()
                    if n in self.converter.load_arg_names
                }
                value = self.converter.load(item_data, context, **kwargs)
        setattr(instance, self.name, value)
        for func in self._after_load_hooks:
            func(instance, context)

    def _get_default(self, instance):
        """Return the default value (for optional fields).

        May be overridden in *instances*.
        """
        return None

    def dump_into(self, instance, data, context):
        """Dump the given Python object into the given JSON-compatible dict

        If the field is not marked `output`, or is optional and has the default
        value, this does nothing.
        """
        if not self.output:
            return
        value = getattr(instance, self.name)
        if self.optional and value == self.default:
            return
        data[self.data_key] = self.converter.dump(value, context)

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

    def default_factory(self):
        """Decorate a function that will be called to produce a default value

        The decorated function will be called with one argument: the instance
        being initialized.
        """
        def _decorator(func):
            self.optional = True
            self._get_default = func
            return func
        return _decorator

    def after_load(self):
        """Decorate a function that will be called after an attribute is loaded

        The decorated function will be called with one argument: the instance
        being initialized. (The Field's attribute will already be set on it.)
        """
        def _decorator(func):
            self._after_load_hooks.append(func)
            return func
        return _decorator


class VersionField(AbstractField):
    """Chooses Field based on the API version

    `fields` should be a {version introduced: field} mapping.
    When loading/dumping/getting schema, VersionField picks the field for
    tat version and forwards the operation to it.
    For versions before the first specified, the field is not loaded/dumped,
    and the instance attribute is set to None.

    VersionField adds a "Added/Modified in API version" note to the JSON Schema
    description.

    Making later fields suitably backwards-compatible is the user's
    responsibility.
    """

    def __init__(self, fields, name=None):
        self.fields = sorted((tuple(k), f) for k, f in fields.items())
        self.name = name

    def _field_for_context(self, context):
        for version, field in reversed(self.fields):
            if version <= context.version:
                return version, field
        return None, None

    def __repr__(self):
        return f'<{_classname(type(self))} {self.name} ({self.fields})>'

    def __set_name__(self, cls, name):
        self.name = name
        for version, field in self.fields:
            set_name = getattr(type(field), '__set_name__', None)
            if set_name:
                set_name(field, cls, name)

    def load_into(self, instance, data, context, **kwargs):
        version, field = self._field_for_context(context)
        if field:
            field.load_into(instance, data, context, **kwargs)
        else:
            setattr(instance, self.name, None)

    def dump_into(self, instance, data, context):
        version, field = self._field_for_context(context)
        if field:
            field.dump_into(instance, data, context)

    def put_schema_into(self, object_schema, context):
        version, field = self._field_for_context(context)
        if field:
            field.put_schema_into(object_schema, context)
            try:
                schema = object_schema['properties'][self.name]
            except KeyError:
                pass
            if version == self.fields[0][0]:
                note = 'Added in API version {}.{}'.format(*version)
            else:
                note = 'Modified in API version {}.{}'.format(*version)
            if 'description' in schema:
                schema['description'] += '\n\n' + note
            else:
                schema['description'] = note

    def default_factory(self):
        raise NotImplementedError('default_factory is not implemented yet')

    def after_load(self):
        raise NotImplementedError('after_load is not implemented yet')


class ModelConverter(BaseConverter):
    """Converter for a Model, i.e. class with several Fields"""
    def __init__(
        self, cls, *, slug=None, load_arg_names=(), extra_fields=(),
    ):
        self.cls = cls
        self.name = cls.__name__
        doc = inspect.getdoc(cls)
        if doc:
            self.doc = doc.strip()
        else:
            self.doc = ''
        self.fields = {}
        self.load_arg_names = load_arg_names
        self.slug = slug

        for name, field in vars(cls).items():
            if name.startswith('__') or not isinstance(field, AbstractField):
                continue
            self.fields[name] = field
        self.fields.update((f.name, f) for f in extra_fields)

    def __repr__(self):
        return f'<{_classname(type(self))} for {_classname(self.cls)}>'

    def load(self, data, context, **kwargs):
        result = self.cls(**kwargs)
        for field in self.fields.values():
            field.load_into(result, data, context, parent=result)
        return result

    def dump(self, value, context):
        result = {}
        for field in self.fields.values():
            field.dump_into(value, result, context)
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


class LoadContext:
    """Holds "global" options for loading data

    `version` is the API version, as a tuple of ints (major, minor).
    """
    def __init__(self, version):
        self.version = tuple(version)


class DumpContext:
    """Holds "global" options for dumping data

    `version` is the API version, as a tuple of ints (major, minor).
    """
    def __init__(self, version):
        self.version = tuple(version)


class SchemaContext:
    """Holds "global" definitions and options for getting a context

    `is_input` determines whether schema for input (data from forks) or output
    (naucse's exported API).

    `version` is the API version, as a tuple of ints (major, minor).
    """
    def __init__(self, *, is_input, version):
        self.definition_refs = {}
        self.definitions = {}
        self.is_input = is_input
        self.version = tuple(version)

    def get_schema(self, converter):
        """Get schema for the given converter

        If the converter has a `slug`, its schema is added to definitions
        (unless already present), and a reference to it is returned.
        Otherwise, the schema is returned.
        """
        if converter.slug:
            if converter not in self.definition_refs:
                key = converter.slug
                if key in self.definitions:
                    raise ValueError(f'duplicate key {key}')
                self.definitions[key] = converter.get_schema(context=self)
                self.definition_refs[converter] = f'#/definitions/{key}'
            return {'$ref': self.definition_refs[converter]}
        return converter.get_schema(self)


def get_schema(converter, *, is_input, version):
    """Get schema for the given converter"""
    converter = get_converter(converter)
    context = SchemaContext(is_input=is_input, version=version)
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
            'description': 'URL to the data (in JSON format)',
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

                Version 0.x means incompatible changes may be done at any
                time. Please coordinate your use of the API with us.
            """).strip(),
        },
    })
    ref = context.get_schema(converter)
    slug = converter.slug or 'data'
    return {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            slug: ref,
            'api_version': {'$ref': '#/definitions/api_version'},
            '$schema': {'type': 'string', 'format': 'uri'},
        },
        'required': [slug, 'api_version'],
        '$schema': 'http://json-schema.org/draft-06/schema#',
        'definitions': context.definitions,
    }


def _get_schema_url(converter, instance):
    if converter.get_schema_url:
        schema_url = converter.get_schema_url(instance, is_input=False)
        if schema_url is not None:
            return schema_url
        raise ValueError(f"{converter}.get_schema_url returned None")
    raise ValueError(f"{converter}.get_schema_url is None")


def dump(instance, converter=None, *, version):
    """Dump a Python object

    If converter is None, the default is used.
    """
    if converter is None:
        converter = get_converter(instance)
    converter = get_converter(converter)
    slug = converter.slug or 'data'
    context = DumpContext(version=version)
    result = {
        'api_version': list(context.version),
        slug: converter.dump(instance, context),
    }
    result['$schema'] = _get_schema_url(converter, instance)
    schema = get_schema(converter, is_input=False, version=context.version)
    jsonschema.validate(result, schema)
    return result


def load(converter, data, **kwargs):
    """Load a Python object from the given data"""
    version = data['api_version']
    converter = get_converter(converter)
    context = LoadContext(version=version)
    schema = get_schema(converter, is_input=True, version=context.version)
    jsonschema.validate(data, schema)
    slug = converter.slug or 'data'
    return converter.load(data[slug], context, **kwargs)


def register_model(cls, converter=None):
    """Assign converter as default for the given class

    If `converter` is not given, a new `ModelConverter` is created.
    """
    if converter is None:
        converter = ModelConverter(cls)
    cls._naucse__converter = converter
    return cls
