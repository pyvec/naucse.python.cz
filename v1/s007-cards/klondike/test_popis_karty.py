import pytest
import klondike


def test_popis_rubem_nahoru():
    karta = 13, 'Pi', False
    assert klondike.popis_karty(karta) == '[???]'


def test_popis_srdcova_kralovna():
    karta = 12, 'Sr', True
    assert klondike.popis_karty(karta) in ['[Q ♥]', '[Q S]']


def test_otoc_kralovnu():
    karta = 12, 'Sr', True
    assert klondike.otoc_kartu(karta, True) == (12, 'Sr', True)
    assert klondike.otoc_kartu(karta, False) == (12, 'Sr', False)


def test_otoc_eso():
    karta = 1, 'Pi', False
    assert klondike.otoc_kartu(karta, True) == (1, 'Pi', True)
    assert klondike.otoc_kartu(karta, False) == (1, 'Pi', False)


# Tohle je testovací vychytávka, kterou zatím neznáme:
# několik testů v jedné funkci
@pytest.mark.parametrize('hodnota,znak', [
    (1, 'A'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, 'X'),
    (11, 'J'),
    (12, 'Q'),
    (13, 'K'),
])
def test_popis_hodnoty(hodnota, znak):
    karta = hodnota, 'Sr', True
    assert klondike.popis_karty(karta) in ['[' + znak + ' ♥]', '[' + znak + ' S]']
