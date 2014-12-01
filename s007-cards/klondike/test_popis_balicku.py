import pytest
import klondike


def test_prazdny_balik():
    assert klondike.popis_balicku([]) == '[   ]'


def test_jedna_karta():
    karta = 12, 'Sr', True
    assert klondike.popis_balicku([karta]) in ['[Q ♥]', '[Q S]']


def test_moc_karet():
    neni_videt = 1, 'Sr', False
    karta = 12, 'Sr', True
    balicek = [neni_videt, neni_videt, neni_videt, karta]
    assert klondike.popis_balicku([karta]) in ['[Q ♥]', '[Q S]']
