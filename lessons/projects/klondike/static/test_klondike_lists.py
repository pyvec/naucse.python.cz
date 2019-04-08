import pytest
import textwrap
import re


@pytest.mark.level(10)
def test_import_popis_balicku():
    from klondike import popis_balicku


@pytest.mark.level(11)
def test_popis_balicku_jedna_karta():
    """Balíček se srdcovou dámou by se měl popsat jako tato karta"""
    from klondike import popis_balicku
    karta = 12, 'Sr', True
    assert popis_balicku([karta]) == '[Q ♥]'


@pytest.mark.level(11)
def test_popis_balicku_moc_karet():
    """Balíček se víc kartama by se měl popsat jako vrchní karta"""
    from klondike import popis_balicku
    rubem_nahoru = 1, 'Sr', False
    karta = 12, 'Sr', True
    balicek = [rubem_nahoru, rubem_nahoru, rubem_nahoru, karta]
    assert popis_balicku(balicek) == '[Q ♥]'


@pytest.mark.level(11)
def test_popis_balicku_rubem_nahoru():
    """Balíček s vrchní kartou rubem nahoru by se měl popsat jako [???]"""
    from klondike import popis_balicku
    rubem_nahoru = 1, 'Sr', False
    karta = 12, 'Sr', True
    balicek = [karta, karta, karta, rubem_nahoru]
    assert popis_balicku(balicek) == '[???]'

@pytest.mark.level(12)
def test_popis_prazdneho_balicku():
    """Prázdný balíček se popisuje pomocí [   ]"""
    from klondike import popis_balicku
    assert popis_balicku([]) == '[   ]'


@pytest.mark.level(20)
def test_import_vytvor_balicek():
    from klondike import vytvor_balicek


@pytest.mark.level(21)
def test_vytvor_balicek_52():
    """Balíček by měl obsahovat 52 karet"""
    from klondike import vytvor_balicek
    assert len(vytvor_balicek()) == 52


@pytest.mark.level(21)
def test_vytvor_balicek_bez_duplikatu():
    """Balíček by neměl obsahovat duplikáty"""
    from klondike import vytvor_balicek
    balicek = vytvor_balicek()
    for karta in balicek:
        assert balicek.count(karta) == 1


@pytest.mark.level(22)
@pytest.mark.parametrize('hodnota', range(2, 14))
def test_vytvor_balicek_pocet_hodnoty(hodnota):
    """Balíček by měl obsahovat 4 karty dané hodnoty"""
    from klondike import vytvor_balicek
    balicek = vytvor_balicek()
    pocet = 0
    for hodnota_karty, barva_karty, je_licem_nahoru in balicek:
        if hodnota_karty == hodnota:
            pocet = pocet + 1
    assert pocet == 4


@pytest.mark.level(22)
@pytest.mark.parametrize('barva', ['Pi', 'Sr', 'Ka', 'Kr'])
def test_vytvor_balicek_pocet_barvy(barva):
    """Balíček by měl obsahovat 13 karet dané barvy"""
    from klondike import vytvor_balicek
    balicek = vytvor_balicek()
    pocet = 0
    for hodnota_karty, barva_karty, je_licem_nahoru in balicek:
        if barva_karty == barva:
            pocet = pocet + 1
    assert pocet == 13


@pytest.mark.level(23)
def test_zamichani():
    """Každá hra by měla být jiná"""
    from klondike import vytvor_balicek
    balicek1 = vytvor_balicek()
    balicek2 = vytvor_balicek()

    # Je šance 1 z 80658175170943878571660636856403766975289505440883277824000000000000,
    # že dva náhodné balíčky budou stejné.
    # Nejspíš je pravděpodobnější, že v průběhu testu odejde počítač,
    # na kterém test běží, než aby se ty karty zamíchaly stejně.
    assert balicek1 != balicek2, 'Karty nejsou zamíchané!'


@pytest.mark.level(30)
def test_import_rozdej_sloupecky():
    from klondike import rozdej_sloupecky


@pytest.mark.level(31)
def test_rozdej_sloupecky_7():
    """Rozdaných sloupečků má být 7"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    balicek = vytvor_balicek()
    sloupecky = rozdej_sloupecky(balicek)
    assert len(sloupecky) == 7


@pytest.mark.level(31)
def test_rozdej_sloupecky_velikost_balicku():
    """V balíčku by měly chybět karty ze sloupečků"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    balicek = vytvor_balicek()
    sloupecky = rozdej_sloupecky(balicek)

    # Ceklový počet karet ve sloupečcích
    velikost_vsech_sloupecku = 0
    for sloupecek in sloupecky:
        velikost_vsech_sloupecku = velikost_vsech_sloupecku + len(sloupecek)

    # Kontrola počtu karet v balíčku
    assert len(balicek) == 52 - velikost_vsech_sloupecku


@pytest.mark.level(31)
def test_rozdej_sloupecky_zvrchu_balicku():
    """Karty by měly být rozdané z konce balíčku"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    balicek = vytvor_balicek()
    kopie_puvodniho_balicku = list(balicek)
    sloupecky = rozdej_sloupecky(balicek)

    assert balicek == kopie_puvodniho_balicku[:len(balicek)]


@pytest.mark.level(31)
def test_rozdej_sloupecky_nechybi_karty():
    """V balíčku a sloupečcích by měly být všechny karty"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    from karty import otoc_kartu
    balicek = vytvor_balicek()
    kopie_puvodniho_balicku = list(balicek)
    sloupecky = rozdej_sloupecky(balicek)

    vsechny_karty = list(balicek)
    for sloupecek in sloupecky:
        for karta in sloupecek:
            vsechny_karty.append(otoc_kartu(karta, False))

    vsechny_karty.sort()
    kopie_puvodniho_balicku.sort()

    assert vsechny_karty == kopie_puvodniho_balicku


@pytest.mark.level(31)
def test_rozdej_sloupecky_balicek_rubem_nahoru():
    """Po rozdání sloupečků by měl celý balíček být rubem nahoru"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    balicek = vytvor_balicek()
    sloupecky = rozdej_sloupecky(balicek)

    for hodnota, barva, je_licem_nahoru in balicek:
        assert not je_licem_nahoru


@pytest.mark.level(32)
@pytest.mark.parametrize('cislo_sloupce', range(7))
def test_rozdej_sloupecky_posledni_licem_nahoru(cislo_sloupce):
    """Poslední karta sloupečku je lícem nahoru"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    balicek = vytvor_balicek()
    sloupecky = rozdej_sloupecky(balicek)
    posledni_karta = sloupecky[cislo_sloupce][-1]
    hodnota, barva, je_licem_nahoru = posledni_karta
    assert je_licem_nahoru


@pytest.mark.level(32)
@pytest.mark.parametrize('cislo_sloupce', range(7))
def test_rozdej_sloupecky_ostatni_rubem_nahoru(cislo_sloupce):
    """Karty pod první kartou sloupečku jsou rubem nahoru"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    balicek = vytvor_balicek()
    sloupecky = rozdej_sloupecky(balicek)
    for karta in sloupecky[cislo_sloupce][:-1]:
        hodnota, barva, je_licem_nahoru = karta
        assert not je_licem_nahoru


@pytest.mark.level(33)
@pytest.mark.parametrize('cislo_sloupce', range(7))
def test_rozdej_sloupecky_velikost(cislo_sloupce):
    """Kontrola velikosti rozdaného sloupečku"""
    from klondike import vytvor_balicek, rozdej_sloupecky
    balicek = vytvor_balicek()
    sloupecky = rozdej_sloupecky(balicek)
    assert len(sloupecky[cislo_sloupce]) == cislo_sloupce + 1


@pytest.mark.level(40)
def test_import_vypis_sloupecky():
    from klondike import vypis_sloupecky


def check_text(got, expected):
    got = re.sub(' +\n', '\n', got)  # odstraní mezery z konců řádků
    print(got)
    assert got.strip() == textwrap.dedent(expected).strip()


@pytest.mark.level(41)
def test_vypis_prazdne_sloupecky(capsys):
    from klondike import vypis_sloupecky
    vypis_sloupecky([[], [], [], [], [], [], [], []])
    out, err = capsys.readouterr()
    check_text(out, "")


@pytest.mark.level(41)
def test_vypis_sloupecky_jedna_karta_rubem_nahoru(capsys):
    from klondike import vypis_sloupecky
    vypis_sloupecky([[(1, 'Pi', False)]] * 7)
    out, err = capsys.readouterr()
    check_text(out, "[???] [???] [???] [???] [???] [???] [???]")


@pytest.mark.level(41)
def test_vypis_sloupecky_po_jedne_karte_licem_nahoru(capsys):
    from klondike import vypis_sloupecky
    vypis_sloupecky([
        [(1, 'Pi', True)],
        [(2, 'Sr', True)],
        [(3, 'Ka', True)],
        [(4, 'Kr', True)],
        [(5, 'Pi', True)],
        [(6, 'Sr', True)],
        [(7, 'Ka', True)],
    ])
    out, err = capsys.readouterr()
    check_text(out, "[A♠ ] [2 ♥] [3 ♦] [4♣ ] [5♠ ] [6 ♥] [7 ♦]")


@pytest.mark.level(42)
def test_vypis_sloupecky_dvou_kartach(capsys):
    from klondike import vypis_sloupecky
    vypis_sloupecky([
        [(1, 'Pi', True), (7, 'Sr', True)],
        [(2, 'Sr', True), (6, 'Ka', True)],
        [(3, 'Ka', True), (5, 'Kr', False)],
        [(4, 'Kr', False), (4, 'Pi', True)],
        [(5, 'Pi', False), (3, 'Sr', True)],
        [(6, 'Sr', True), (2, 'Ka', True)],
        [(7, 'Ka', True), (1, 'Kr', True)],
    ])
    out, err = capsys.readouterr()
    check_text(out, """
        [A♠ ] [2 ♥] [3 ♦] [???] [???] [6 ♥] [7 ♦]
        [7 ♥] [6 ♦] [???] [4♠ ] [3 ♥] [2 ♦] [A♣ ]
    """)


@pytest.mark.level(42)
def test_vypis_sloupecky_vice_karet(capsys):
    from klondike import vypis_sloupecky
    vypis_sloupecky([
        [(1, 'Pi', True)],
        [(2, 'Pi', True), (2, 'Sr', True)],
        [(3, 'Pi', True), (3, 'Sr', True), (3, 'Ka', True)],
        [(4, 'Pi', True), (4, 'Sr', True), (4, 'Ka', False), (4, 'Kr', True)],
        [(5, 'Pi', True), (5, 'Sr', True), (5, 'Ka', True)],
        [(6, 'Pi', True), (6, 'Sr', True)],
        [(7, 'Pi', True)],
    ])
    out, err = capsys.readouterr()
    check_text(out, """
        [A♠ ] [2♠ ] [3♠ ] [4♠ ] [5♠ ] [6♠ ] [7♠ ]
              [2 ♥] [3 ♥] [4 ♥] [5 ♥] [6 ♥]
                    [3 ♦] [???] [5 ♦]
                          [4♣ ]
    """)


@pytest.mark.level(50)
def test_import_presun_kartu():
    from klondike import presun_kartu


@pytest.mark.level(51)
def test_presun_kartu_licem_nahoru():
    """Kontrola přesunutí karty, co je na začátku lícem nahoru"""
    from klondike import presun_kartu
    zdroj = [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (5, 'Kr', False),
    ]
    cil = [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
    ]
    presun_kartu(zdroj, cil, True)
    assert zdroj == [
        (3, 'Kr', False),
        (4, 'Sr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
        (5, 'Kr', True),
    ]
    presun_kartu(zdroj, cil, False)
    assert zdroj == [
        (3, 'Kr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
        (5, 'Kr', True),
        (4, 'Sr', False),
    ]


@pytest.mark.level(51)
def test_presun_kartu_rubem_nahoru():
    """Kontrola přesunutí karty, co je na začátku rubem nahoru"""
    from klondike import presun_kartu
    zdroj = [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
    ]
    cil = [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (5, 'Kr', False),
    ]
    presun_kartu(zdroj, cil, True)
    assert zdroj == [
        (11, 'Pi', True),
        (12, 'Ka', True),
    ]
    assert cil == [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (5, 'Kr', False),
        (13, 'Pi', True),
    ]
    presun_kartu(zdroj, cil, False)
    assert zdroj == [
        (11, 'Pi', True),
    ]
    assert cil == [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (5, 'Kr', False),
        (13, 'Pi', True),
        (12, 'Ka', False),
    ]


@pytest.mark.level(60)
def test_import_presun_nekolik_karet():
    from klondike import presun_nekolik_karet


@pytest.mark.level(61)
def test_presun_jednu_kartu():
    """Zkontroluje přesunutí jedné karty pomocí presun_nekolik_karet"""
    from klondike import presun_nekolik_karet
    zdroj = [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (5, 'Kr', False),
    ]
    cil = [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
    ]
    presun_nekolik_karet(zdroj, cil, 1)
    assert zdroj == [
        (3, 'Kr', False),
        (4, 'Sr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
        (5, 'Kr', False),
    ]


@pytest.mark.level(61)
def test_presun_dve_karty():
    """Zkontroluje přesunutí dvou karet najednou"""
    from klondike import presun_nekolik_karet
    zdroj = [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (5, 'Kr', False),
    ]
    cil = [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
    ]
    presun_nekolik_karet(zdroj, cil, 2)
    assert zdroj == [
        (3, 'Kr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
        (4, 'Sr', False),
        (5, 'Kr', False),
    ]


@pytest.mark.level(61)
def test_presun_tam_a_zpet():
    """Zkontroluje přesouvání karet tam a zpátky"""
    from klondike import presun_nekolik_karet
    zdroj = [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (5, 'Kr', False),
    ]
    cil = [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
    ]
    presun_nekolik_karet(zdroj, cil, 1)
    assert zdroj == [
        (3, 'Kr', False),
        (4, 'Sr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (13, 'Pi', True),
        (5, 'Kr', False),
    ]
    presun_nekolik_karet(cil, zdroj, 2)
    assert zdroj == [
        (3, 'Kr', False),
        (4, 'Sr', False),
        (13, 'Pi', True),
        (5, 'Kr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
        (12, 'Ka', True),
    ]
    presun_nekolik_karet(zdroj, cil, 3)
    assert zdroj == [
        (3, 'Kr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
        (12, 'Ka', True),
        (4, 'Sr', False),
        (13, 'Pi', True),
        (5, 'Kr', False),
    ]
    presun_nekolik_karet(cil, zdroj, 4)
    assert zdroj == [
        (3, 'Kr', False),
        (12, 'Ka', True),
        (4, 'Sr', False),
        (13, 'Pi', True),
        (5, 'Kr', False),
    ]
    assert cil == [
        (11, 'Pi', True),
    ]
    presun_nekolik_karet(zdroj, cil, 5)
    assert zdroj == [
    ]
    assert cil == [
        (11, 'Pi', True),
        (3, 'Kr', False),
        (12, 'Ka', True),
        (4, 'Sr', False),
        (13, 'Pi', True),
        (5, 'Kr', False),
    ]
