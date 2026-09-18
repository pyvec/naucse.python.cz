import pytest
import karty


def test_popis_rubem_nahoru():
    """Popis karty, která je rubem nahoru, by měl ukázat otazníky"""
    karta = 13, 'Pi', False
    assert karty.popis_kartu(karta) == '[???]'


def test_popis_srdcova_kralovna():
    """Popis srdcové královny by měl být "[Q ♥]"."""
    karta = 12, 'Sr', True
    assert karty.popis_kartu(karta) == '[Q ♥]'


def test_popis_krizova_sestka():
    """Popis křížové šestky by měl být "[6♣ ]"."""
    karta = 6, 'Kr', True
    assert karty.popis_kartu(karta) == '[6♣ ]'


def test_popis_karova_desitka():
    """Popis kárové desítky by měl být "[X ♦]"."""
    karta = 10, 'Ka', True
    assert karty.popis_kartu(karta) == '[X ♦]'


def test_popis_pikove_eso():
    """Popis pikového esa by měl být "[A♠ ]"."""
    karta = 1, 'Pi', True
    assert karty.popis_kartu(karta) == '[A♠ ]'


def test_otoc_kralovnu():
    """Kontrola otočení karty, co je na začátku lícem nahoru"""
    karta = 12, 'Sr', True
    assert karty.otoc_kartu(karta, True) == (12, 'Sr', True)
    assert karty.otoc_kartu(karta, False) == (12, 'Sr', False)


def test_otoc_eso():
    """Kontrola otočení karty, co je na začátku rubem nahoru"""
    karta = 1, 'Pi', False
    assert karty.otoc_kartu(karta, True) == (1, 'Pi', True)
    assert karty.otoc_kartu(karta, False) == (1, 'Pi', False)


# Tohle je testovací vychytávka, kterou zatím neznáme:
# několik podobných testů zadaných jednou funkcí
PRIKLADY = [
    (1, 'Ka', '[A ♦]'),
    (2, 'Ka', '[2 ♦]'),
    (3, 'Sr', '[3 ♥]'),
    (4, 'Sr', '[4 ♥]'),
    (5, 'Kr', '[5♣ ]'),
    (6, 'Pi', '[6♠ ]'),
    (7, 'Ka', '[7 ♦]'),
    (8, 'Kr', '[8♣ ]'),
    (9, 'Sr', '[9 ♥]'),
    (10, 'Kr', '[X♣ ]'),
    (11, 'Ka', '[J ♦]'),
    (12, 'Sr', '[Q ♥]'),
    (13, 'Kr', '[K♣ ]'),
]
@pytest.mark.parametrize(['hodnota', 'barva', 'pozadovany_popis'], PRIKLADY)
def test_popis_hodnoty(hodnota, barva, pozadovany_popis):
    """Kontrola popisu karty"""
    karta = hodnota, barva, True
    assert karty.popis_kartu(karta) == pozadovany_popis
