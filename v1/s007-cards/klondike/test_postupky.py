import klondike
import pytest


@pytest.mark.parametrize('barva', ('Pi', 'Ka', 'Sr', 'Kr'))
def test_jedne_barvy(barva):
    karty = [
        (4, barva, False),
        (3, barva, False),
        (2, barva, False),
    ]
    with pytest.raises(ValueError):
        # 'Musíš střídat barvy!'
        klondike.zkontroluj_postupku(karty)


@pytest.mark.parametrize('barva', ('Pi', 'Ka', 'Sr', 'Kr'))
def test_jedne_karty(barva):
    karty = [
        (6, barva, False),
    ]
    klondike.zkontroluj_postupku(karty)


@pytest.mark.parametrize('hodnota', range(1, 14))
def test_stejnych_hodnot(hodnota):
    karty = [
        (hodnota, 'Pi', False),
        (hodnota, 'Ka', False),
        (hodnota, 'Kr', False),
        (hodnota, 'Sr', False),
    ]
    with pytest.raises(ValueError):
        # 'Musíš dělat sestupné postupky!'
        klondike.zkontroluj_postupku(karty)


def test_ok():
    karty = [
        (11, 'Pi', False),
        (10, 'Ka', False),
        (9, 'Kr', False),
        (8, 'Sr', False),
    ]
    klondike.zkontroluj_postupku(karty)


def test_vzestupna():
    karty = [
        (8, 'Pi', False),
        (9, 'Ka', False),
        (10, 'Kr', False),
        (11, 'Sr', False),
    ]
    with pytest.raises(ValueError):
        # 'Musíš dělat sestupné postupky!'
        klondike.zkontroluj_postupku(karty)


def test_nestridani_barev():
    karty = [
        (11, 'Pi', False),
        (10, 'Ka', False),
        (9, 'Sr', False),
        (8, 'Kr', False),
    ]
    with pytest.raises(ValueError):
        # 'Musíš střídat barvy!'
        klondike.zkontroluj_postupku(karty)
