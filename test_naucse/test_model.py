from pathlib import Path
import os

import pytest
import yaml

from naucse import models
from naucse.edit_info import get_local_repo_info


fixture_path = Path(__file__).parent / 'fixtures'


def dummy_schema_url_factory(cls, **kwargs):
    return f'http://dummy.test/schema/{cls.__name__}'


class DummyURLFactories:
    def __getitem__(self, cls):
        def dummy_url_factory(_external=True, **kwargs):
            args = '&'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))
            return f'http://dummy.test/model/{cls.__name__}/?{args}'
        return dummy_url_factory


def assert_matches_expected_dump(data, filename):
    yaml_path = fixture_path / 'expected-dumps' / filename
    try:
        expected_yaml = yaml_path.read_text()
    except FileNotFoundError:
        expected_yaml = ''
        expected = None
    else:
        expected = yaml.safe_load(expected_yaml)
    if data != expected or expected is None:
        # I find that textually comparing structured dumped to YAML is easier
        # than a "deep diff" algorithm (like the one in pytest).
        # To make this easier, running in a special mode will dump the expected
        # YAML to the given file. Changes can then be verified with `git diff`.
        data_dump = yaml.safe_dump(data, default_flow_style=False, indent=4)
        if os.environ.get('TEST_NAUCSE_DUMP_YAML') == '1':
            yaml_path.write_text(data_dump)
        else:
            print(
                'Note: Run with TEST_NAUCSE_DUMP_YAML=1 to dump the '
                'expected YAML'
            )
        assert data_dump == expected_yaml
        assert data == expected


def test_empty_model():
    model = models.Root()
    assert not model.courses
    assert not model.licenses
    assert not model.run_years
    assert model.get_pks() == {}

    with pytest.raises(models.NoURL):
        model.get_url()


def test_licenses():
    model = models.Root()
    model.load_licenses(fixture_path / 'licenses')

    assert sorted(model.licenses) == ['cc-by-sa-40', 'cc0']
    assert model.licenses['cc0'].slug == 'cc0'
    assert model.licenses['cc0'].url.endswith('/publicdomain/zero/1.0/')
    assert model.licenses['cc0'].title.endswith('Public Domain Dedication')

    assert model.licenses['cc-by-sa-40'].slug == 'cc-by-sa-40'
    assert model.licenses['cc-by-sa-40'].url.endswith('/licenses/by-sa/4.0/')
    assert model.licenses['cc-by-sa-40'].title.endswith('4.0 International')


def test_dump_empty_model():
    model = models.Root(schema_url_factory=dummy_schema_url_factory)
    assert_matches_expected_dump(models.dump(model), 'empty-root.yml')


def test_load_empty_dir():
    model = models.Root()
    with pytest.raises(FileNotFoundError):
        model.load_local_courses(fixture_path / 'empty-directory')

    assert not model.courses


def test_no_courses():
    """Loading directory with no courses gives only an empty "lessons" course
    """
    model = models.Root()
    model.load_local_courses(fixture_path / 'empty-lessons-dir')

    assert sorted(model.courses) == ['lessons']
    assert not model.courses['lessons'].sessions
    assert not model.courses['lessons'].lessons


def test_load_courses():
    model = models.Root()
    model.load_local_courses(fixture_path / 'minimal-courses')

    assert sorted(model.courses) == [
        '2019/minimal', 'courses/minimal', 'lessons',
    ]

    assert model.courses['courses/minimal'].title == 'A minimal course'
    assert model.courses['courses/minimal'].slug == 'courses/minimal'
    assert model.courses['2019/minimal'].title == 'A minimal course'
    assert model.courses['2019/minimal'].slug == '2019/minimal'
    assert model.courses['lessons'].title == 'Kanonické lekce'
    assert model.courses['lessons'].slug == 'lessons'


def test_add_local_course():
    model = models.Root()
    path = fixture_path / 'minimal-courses'
    model.add_course(models.Course.load_local(
        parent=model,
        path=path,
        repo_info=get_local_repo_info(path),
        slug='courses/minimal',
    ))

    assert sorted(model.courses) == ['courses/minimal']

    assert model.courses['courses/minimal'].title == 'A minimal course'
    assert model.courses['courses/minimal'].slug == 'courses/minimal'


def test_dump_local_course():
    model = models.Root(
        schema_url_factory=dummy_schema_url_factory,
        url_factories={
            'api': DummyURLFactories(),
        },
    )
    path = fixture_path / 'minimal-courses'
    model.add_course(models.Course.load_local(
        parent=model,
        path=path,
        repo_info=get_local_repo_info(path),
        slug='courses/minimal',
    ))

    assert_matches_expected_dump(models.dump(model), 'minimal-root.yml')
    course = model.courses['courses/minimal']
    assert_matches_expected_dump(models.dump(course), 'minimal-course.yml')


def test_add_course_from_data():
    model = models.Root()

    model.add_course(models.load(
        models.Course,
        slug='courses/minimal',
        repo_info=get_local_repo_info(fixture_path),
        parent=model,
        data={
            'api_version': [0, 0],
            'course': {
                'title': 'A minimal course',
                'sessions': [],
            },
        },
    ))

    assert sorted(model.courses) == ['courses/minimal']

    assert model.courses['courses/minimal'].title == 'A minimal course'
    assert model.courses['courses/minimal'].slug == 'courses/minimal'
