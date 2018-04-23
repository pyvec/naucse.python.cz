from collections import OrderedDict
from pathlib import Path

import yaml
from arca import Task, Arca
from werkzeug.local import LocalProxy

import naucse.utils.views

_arca = None


@LocalProxy
def arca():
    global _arca
    if _arca is not None:
        return _arca

    _arca = Arca(settings={"ARCA_BACKEND": "arca.backend.CurrentEnvironmentBackend",
                           "ARCA_BACKEND_CURRENT_ENVIRONMENT_REQUIREMENTS": "requirements.txt",
                           "ARCA_BACKEND_VERBOSITY": 2,
                           # required by PyNaCl which is required by Gabric3 which is required by Arca
                           # only needed for Arcas Vagrant backend, can be removed once Arca
                           # implements optional requirements
                           "ARCA_BACKEND_APK_DEPENDENCIES": ["libffi-dev"],
                           "ARCA_BACKEND_KEEP_CONTAINER_RUNNING": True,
                           "ARCA_BACKEND_USE_REGISTRY_NAME": "docker.io/naucse/naucse.python.cz",
                           "ARCA_SINGLE_PULL": True,
                           "ARCA_IGNORE_CACHE_ERRORS": True,
                           "ARCA_CACHE_BACKEND": "dogpile.cache.dbm",
                           "ARCA_CACHE_BACKEND_ARGUMENTS": {
                               "filename": ".arca/cache/naucse.dbm"
                           }})

    return _arca


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


class ForkProperty(LazyProperty):
    """Populated from the fork the model is pointing to.

    ``repo`` and ``branch`` indicate from which attribute of the instance
    the property should take info about the fork.

    ``**kwargs`` are for `arca.Task`. The values can be callable, in which
    case they are called with the instance as a parameter.
    """
    def __init__(self, repo, branch, **kwargs):
        self.repo_prop = repo
        self.branch_prop = branch
        self.kwargs = kwargs

    def process_kwargs(self, instance):
        x = {}

        for key, value in self.kwargs.items():
            if callable(value):
                value = value(instance)

            x[key] = value

        return x

    def compute(self, instance):
        naucse.utils.views.forks_raise_if_disabled()

        task = Task(**self.process_kwargs(instance))

        result = arca.run(getattr(instance, self.repo_prop.name), getattr(instance, self.branch_prop.name), task,
                          reference=Path("."), depth=None)

        return result.output


class DataProperty:
    """Value retreived from a YamlProperty

    If ``key`` is not given, this property's name is used.
    ``convert`` can be used to convert the value to something else.
    """
    def __init__(self, dict_prop, *, key=NOTHING, default=NOTHING, convert=NOTHING):
        self.dict_prop = dict_prop
        self.key = key
        self.default = default
        self.convert = convert

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
            val = info[key]
        else:
            val = info.get(key, self.default)

        if self.convert is NOTHING or not callable(self.convert):
            return val

        return self.convert(val)


class DirProperty(LazyProperty):
    """Ordered dict of models from a subdirectory

    If ``info.yml`` is present in the subdirectory, it must contain a dict
    with an "order" key, which is used to order the models.
    The rest is appended in alphabetical order.

    If ``keyfunc`` is given, it is used to create keys from directory names.
    The default is ``str``, i.e. the directory name is used as dict key.
    """
    def __init__(self, cls, *subdir, keyfunc=str):
        self.cls = cls
        self.subdir = subdir
        self.keyfunc = keyfunc

    def get_ordered_dirs(self, base):
        model_paths = []

        info_path = base.joinpath("info.yml")
        if info_path.is_file():
            with info_path.open(encoding='utf-8') as f:
                model_paths = [base.joinpath(p) for p in yaml.safe_load(f)['order']]

        remaining_subdirectories = [p for p in sorted(base.iterdir()) if p.is_dir() and p not in model_paths]

        return model_paths + remaining_subdirectories

    def compute(self, instance):
        base = instance.path.joinpath(*self.subdir)

        dirs = self.get_ordered_dirs(base)

        return OrderedDict(
            (self.keyfunc(p.parts[-1]), self.cls(instance.root, p))
            for p in dirs
        )


class MultipleModelDirProperty(DirProperty):
    """Ordered dict of models from a subdirectory.

    For directories that have different models inside of them.

    The models which are supposed to be used are defined by files they
    load their content out of and the definition prioritizes them - first
    come first serve.
    If none of the models is present in the folders, an exception is raised.
    Each of the models must have an attribute ``data_filename`` with
    the filename used for defining them.

    The prioritization is important in forks, since many directories
    contain both info.yml and link.yml.

    Possible to order by ``info.yml`` just like DirProperty.
    """
    def __init__(self, classes, *subdir, keyfunc=str):
        self.classes = list(classes)

        for cls in self.classes:
            if not hasattr(cls, "data_filename"):
                raise ValueError(f"The model {cls.__name__} doesn't have a data_filename attribute.")

        super().__init__(None, *subdir, keyfunc=keyfunc)

    def compute(self, instance):
        base = instance.path.joinpath(*self.subdir)

        dirs = self.get_ordered_dirs(base)

        models = []

        for path in dirs:  # type: Path
            selected_class = None

            for cls in self.classes:
                if (path / cls.data_filename).exists():
                    selected_class = cls
                    break

            if selected_class is None:
                raise ValueError(f"There are no model definition files in {path.resolve()}")

            models.append(
                (self.keyfunc(path.parts[-1]), selected_class(instance.root, path))
            )

        return OrderedDict(models)


class reify(LazyProperty):
    """Reify decorator, as known from Pyramid"""
    def __init__(self, func):
        self.compute = func
