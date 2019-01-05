from pathlib import Path
import os

import pytest
import yaml

from naucse import models
from naucse.edit_info import get_local_repo_info

from test_naucse.conftest import fixture_path, dummy_schema_url_factory
from test_naucse.conftest import assert_yaml_dump, add_test_course


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
    assert_yaml_dump(models.dump(model), 'empty-root.yml')


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


def test_dump_local_course(model):
    path = fixture_path / 'minimal-courses'
    model.add_course(models.Course.load_local(
        parent=model,
        path=path,
        repo_info=get_local_repo_info(path),
        slug='courses/minimal',
    ))

    assert_yaml_dump(models.dump(model), 'minimal-root.yml')
    course = model.courses['courses/minimal']
    assert_yaml_dump(models.dump(course), 'minimal-course.yml')


def test_add_course_from_data():
    model = models.Root()

    add_test_course(model, 'courses/minimal', {
        'title': 'A minimal course',
        'sessions': [],
    })

    assert sorted(model.courses) == ['courses/minimal']

    assert model.courses['courses/minimal'].title == 'A minimal course'
    assert model.courses['courses/minimal'].slug == 'courses/minimal'
