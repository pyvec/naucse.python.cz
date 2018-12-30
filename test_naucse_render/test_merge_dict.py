import pytest

from naucse_render.course import merge_dict


def test_scalars():
    assert merge_dict(
         {'a': 1, 'b': 2},
         {'b': 5, 'c': 6},
    ) == {'a': 1, 'b': 5, 'c': 6}


def test_subdict():
    assert merge_dict(
         {'subdict': {'a': 1, 'b': 2}},
         {'subdict': {'b': 5, 'c': 6}},
    ) == {'subdict': {'a': 1, 'b': 5, 'c': 6}}


def test_sublist_merge():
    assert merge_dict(
         {'sublist': [1, 2, 3]},
         {'sublist': [4, 5, 6]},
    ) == {'sublist': [4, 5, 6]}


def test_sublist_with_merge():
    assert merge_dict(
         {'sublist': [1, 2, 3]},
         {'sublist': [0, '+merge', 4]},
    ) == {'sublist': [0, 1, 2, 3, 4]}


def test_not_incompatible_types_dict():
    with pytest.raises(TypeError):
        assert merge_dict(
            {'item': 123},
            {'item': {'b': 5, 'c': 6}},
        )


def test_not_incompatible_types_list():
    with pytest.raises(TypeError):
        assert merge_dict(
            {'item': 123},
            {'item': [0, '+merge', 4]},
        )
