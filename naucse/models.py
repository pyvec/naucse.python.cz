from collections import OrderedDict

from naucse.modelutils import Model, YamlProperty, DataProperty, DirProperty, reify
from naucse.modelutils import reify

class Lesson(Model):
    """An individual lesson stored on naucse"""
    def __str__(self):
        return '{} - {}'.format(self.slug, self.title)

    info = YamlProperty()

    title = DataProperty(info)
    style = DataProperty(info)
    css = DataProperty(info, default=None)

    jinja = DataProperty(info, default=False)

    @reify
    def attributions(self):
        attr = self.info.get('attribution', ())
        if isinstance(attr, str):
            attr = [attr]
        return tuple(attr)

    @reify
    def license(self):
        if self.info.get('license') is None:
            return None
        return self.root.licenses[self.info['license']]

    @reify
    def slug(self):
        return '/'.join(self.path.parts[-2:])


class Collection(Model):
    """An collection of lessons"""
    def __str__(self):
        return self.path.parts[-1]

    lessons = DirProperty(Lesson)


class Material(Model):
    """An link – either a lesson, or an external URL"""
    def __init__(self, root, path, info, base_collection):
        super().__init__(root, path)
        self.info = info
        self.base_collection = base_collection

    def __str__(self):
        return self.title

    @reify
    def url(self):
        return self.info['url']

    @reify
    def lesson(self):
        try:
            name = self.info['lesson']
        except KeyError:
            return None
        else:
            return self.root.get_lesson(name, self.base_collection)

    @reify
    def title(self):
        try:
            return self.info['title']
        except KeyError:
            pass
        return self.lesson.title


class Session(Model):
    """An ordered collection of materials"""
    def __init__(self, root, path, info, base_collection=None):
        super().__init__(root, path)
        self.info = info
        self.base_collection = base_collection

    def __str__(self):
        return self.title

    info = YamlProperty()

    title = DataProperty(info)
    slug = DataProperty(info)
    date = DataProperty(info, default=None)

    @reify
    def materials(self):
        return [Material(self.root, self.path, s, self.base_collection)
                for s in self.info['materials']]


def _get_sessions(model, plan, base_collection):
    result = OrderedDict(
        (s['slug'],
            Session(model.root, model.path, s, base_collection))
        for s in plan
    )
    if len(result) != len(set(result)):
        raise ValueError('slugs not unique in {!r}'.format(model))
    return result


class Course(Model):
    """A course – ordered collection of sessions"""
    def __str__(self):
        return self.slug

    info = YamlProperty()

    title = DataProperty(info)
    description = DataProperty(info)
    long_description = DataProperty(info)

    @reify
    def slug(self):
        return self.path.parts[-1]

    @reify
    def sessions(self):
        base_collection = self.info.get('base_collection')
        return _get_sessions(self, self.info['plan'], base_collection)


class Run(Model):
    """A run"""
    def __str__(self):
        return '{} - {}'.formta(self.slug, self.title)

    info = YamlProperty()

    title = DataProperty(info)
    subtitle = DataProperty(info)
    description = DataProperty(info)
    long_description = DataProperty(info)

    @reify
    def sessions(self):
        base_collection = self.info.get('base_collection')
        return _get_sessions(self, self.info['plan'], base_collection)

    @reify
    def slug(self):
        return '/'.join(self.path.parts[-2:])


class RunYear(Model):
    """A year of runs"""
    def __str__(self):
        return self.path.parts[-1]

    runs = DirProperty(Run)


class License(Model):
    def __str__(self):
        return self.path.parts[-1]

    info = YamlProperty()

    title = DataProperty(info)
    url = DataProperty(info)


class Root(Model):
    """The base of the model"""
    def __init__(self, path):
        super().__init__(self, path)

    collections = DirProperty(Collection, 'lessons')
    courses = DirProperty(Course, 'courses')
    run_years = DirProperty(RunYear, 'runs', keyfunc=int)
    licenses = DirProperty(License, 'licenses')

    @reify
    def runs(self):
        return {
            (year, slug): run
            for year, run_year in self.run_years.items()
            for slug, run in run_year.runs.items()
        }

    def get_lesson(self, name, base_collection=None):
        if '/' in name:
            base_collection, name = name.split('/', 2)
        collection = self.collections[base_collection]
        return collection.lessons[name]
