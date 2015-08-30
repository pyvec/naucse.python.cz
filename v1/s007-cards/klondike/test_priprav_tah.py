import klondike
import pytest


def udelej_vzorovou_hru():
    return (([
        (8, 'Pi', False),
        (4, 'Pi', False),
        (12, 'Sr', False),
        (11, 'Sr', False),
        (10, 'Ka', False),
        (2, 'Kr', False),
        (2, 'Sr', False),
        (10, 'Pi', False),
        (1, 'Sr', False),
        (13, 'Sr', False),
        (9, 'Sr', False),
        (1, 'Pi', False),
        (2, 'Pi', False),
        (9, 'Kr', False),
        (6, 'Pi', False),
        (4, 'Ka', False),
        (13, 'Kr', False),
        (8, 'Sr', False),
        (9, 'Ka', False),
        (12, 'Pi', False),
        (10, 'Kr', False),
        (3, 'Kr', False),
        (11, 'Ka', False),
        (5, 'Sr', False)
    ], []), ([], [], [], []), (
        [(7, 'Pi', True)],
        [(13, 'Pi', False), (7, 'Ka', True)],
        [(1, 'Ka', False), (5, 'Pi', False), (9, 'Pi', True)],
        [(8, 'Kr', False), (7, 'Sr', False), (5, 'Kr', False), (8, 'Ka', True)],
        [
            (6, 'Ka', False),
            (10, 'Sr', False),
            (4, 'Sr', False),
            (12, 'Ka', False),
            (3, 'Pi', True)
        ],
        [
            (5, 'Ka', False),
            (11, 'Pi', False),
            (2, 'Ka', False),
            (12, 'Kr', False),
            (3, 'Sr', False),
            (11, 'Kr', True)
        ],
        [
            (1, 'Kr', False),
            (6, 'Kr', False),
            (13, 'Ka', False),
            (7, 'Kr', False),
            (6, 'Sr', False),
            (3, 'Ka', False),
            (4, 'Kr', True),
        ]
    ))


def test_vic_karet_z_v():
    hra = udelej_vzorovou_hru()
    hra[0][1].extend([(6, 'Sr', True), (5, 'Pi', True)])
    with pytest.raises(ValueError):
        # Z balíčku V se nedá brát víc karet najednou!'
        klondike.priprav_tah(hra, (7, 2, 0))


def test_neni_dost_karet_ve_v():
    hra = udelej_vzorovou_hru()
    with pytest.raises(ValueError):
        # 'Na to není v V dost karet!'
        klondike.priprav_tah(hra, (7, 2, 0))


def test_neni_dost_karet_v_b():
    hra = udelej_vzorovou_hru()
    hra[2][1][:] = [(6, 'Sr', True), (5, 'Pi', True)]
    with pytest.raises(ValueError):
        # 'Na to není v B dost karet!'
        klondike.priprav_tah(hra, (1, 4, 0))


def test_presun_rubem_nahoru():
    hra = udelej_vzorovou_hru()
    hra[2][1][:] = [(6, 'Sr', False), (5, 'Pi', True)]
    with pytest.raises(ValueError):
        # 'Nemůžeš přesouvat karty, které jsou rubem nahoru!'
        klondike.priprav_tah(hra, (1, 2, 0))


def test_sedma_na_prazdny_sloupecek():
    hra = udelej_vzorovou_hru()
    hra[2][0].clear()
    with pytest.raises(ValueError):
        # 'Do prázdného sloupečku smí jen král!'
        klondike.priprav_tah(hra, (1, 1, 0))


def test_vic_karet_do_cile():
    hra = udelej_vzorovou_hru()
    hra[2][0][:] = [(2, 'Pi', True), (1, 'Pi', True)]
    with pytest.raises(ValueError):
        # 'Do cíle se nedá dávat víc karet najednou!'
        klondike.priprav_tah(hra, (0, 2, 7))


def test_dvojka_do_prazdneho_cile():
    hra = udelej_vzorovou_hru()
    hra[2][0][:] = [(1, 'Pi', True), (2, 'Pi', True)]
    with pytest.raises(ValueError):
        # 'Do cíle se nedá dávat víc karet najednou!'
        klondike.priprav_tah(hra, (0, 1, 7))


def test_spatna_barva_do_cile():
    hra = udelej_vzorovou_hru()
    hra[1][0].append((1, 'Pi', True))
    hra[2][0].append((2, 'Kr', True))
    with pytest.raises(ValueError):
        # 'Cílová hromádka musí mít jednu barvu!'
        klondike.priprav_tah(hra, (0, 1, 7))


def test_spatna_hodnota_do_cile():
    hra = udelej_vzorovou_hru()
    hra[1][0].append((1, 'Pi', True))
    hra[2][0].append((3, 'Pi', True))
    with pytest.raises(ValueError):
        # 'Do cíle musíš skládat karty postupně od nejnižších!'
        klondike.priprav_tah(hra, (0, 1, 7))
