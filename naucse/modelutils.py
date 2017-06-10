from collections import OrderedDict
from pathlib import Path
import sys

import yaml


NOTHING = object()


class Model:
    def __init__(self, root, path):
        self.root = root
        self.path = Path(path)

    def __str__(self):
        return '0x{:x}'.format(id(self))

    def __repr__(self):
        cls = type(self)
        return '<{}.{}: {}>'.format(cls.__module__, cls.__qualname__,
                                    str(self))


class LazyProperty:
    """Base class for a lazily computed property

    Subclasses should reimplement a `compute` method, which creates
    the value of the property. Then the value is stored and not computed again
    (unless deleted).
    """
    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        result = self.compute(instance)
        setattr(instance, self.name, result)
        return result

    def compute(self, instance):
        raise NotImplementedError()


class YamlProperty(LazyProperty):
    """Populated with the contents of a YAML file.

    If ``filename`` is not given, it is generated from the property's name.
    """
    def __init__(self, *, filename=None):
        self.filename = filename

    def compute(self, instance):
        filename = self.filename
        if filename is None:
            filename = self.name + '.yml'
        with instance.path.joinpath(filename).open(encoding='utf-8') as f:
            return yaml.safe_load(f)


class DataProperty:
    """Value retreived from a YamlProperty

    If ``key`` is not given, this property's name is used.
    """
    def __init__(self, dict_prop, *, key=NOTHING, default=NOTHING):
        self.dict_prop = dict_prop
        self.key = key
        self.default = default

    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        key = self.key
        if key is NOTHING:
            key = self.name
        info = getattr(instance, self.dict_prop.name)
        if self.default is NOTHING:
            return info[key]
        else:
            return info.get(key, self.default)


class DirProperty(LazyProperty):
    """Ordered dict of models from a subdirectory
    
    If ``info.yml`` is present in the subdirectory, use it for the order
    of the models.  The rest is appended alphabetically.
    """
    def __init__(self, cls, *subdir, keyfunc=str):
        self.cls = cls
        self.subdir = subdir
        self.keyfunc = keyfunc

    def compute(self, instance):
        base = instance.path.joinpath(*self.subdir)
        
        model_paths = []
        info_path = base.joinpath("info.yml")
        if info_path.is_file():
            with info_path.open(encoding='utf-8') as f:
                model_paths = [base.joinpath(p) for p in yaml.safe_load(f)]
        
        subdirectories = [p for p in sorted(base.iterdir()) if p.is_dir()]
        return OrderedDict(
            (self.keyfunc(p.parts[-1]), self.cls(instance.root, p))
            for p in model_paths + subdirectories
        )


class reify(LazyProperty):
    """Reify decorator, as known from Pyramid"""
    def __init__(self, func):
        self.compute = func


if sys.version_info < (3, 6):
    # Hack to make __set_name__ work in Python 3.5 and below
    class SettingDict(dict):
        def __setitem__(self, name, item):
            super().__setitem__(name, item)
            try:
                set_name = item.__set_name__
            except AttributeError:
                pass
            else:
                set_name(None, name)

    class ModelMeta(type):
        def __prepare__(meta, cls):
            return SettingDict()

    class Model(Model, metaclass=ModelMeta):
        pass
