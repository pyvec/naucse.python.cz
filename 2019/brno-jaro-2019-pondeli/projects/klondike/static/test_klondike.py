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


@pytest.mark.level(25)
def test_import_popis_seznam_karet():
    from klondike import popis_seznam_karet


@pytest.mark.level(26)
def test_popis_seznam_karet():
    from klondike import popis_seznam_karet
    karty = [
        (13, 'Pi', True),
        (12, 'Sr', True),
        (11, 'Ka', True),
        (10, 'Kr', False)
    ]
    assert popis_seznam_karet([]) == ''


@pytest.mark.level(27)
def test_popis_prazdny_seznam_karet():
    from klondike import popis_seznam_karet
    assert popis_seznam_karet([]) == ''


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


@pytest.mark.level(42)
def test_vypis_sloupecky_ruby(capsys):
    """Kontrola výpisu sloupečků, kde jsou všechny karty rubem nahoru"""
    from klondike import vypis_sloupecky
    sloupecky = [
        [(13, 'Pi', False)] * 2,
        [(13, 'Pi', False)] * 3,
        [(13, 'Pi', False)] * 4,
        [(13, 'Pi', False)] * 5,
        [(13, 'Pi', False)] * 6,
        [(13, 'Pi', False)] * 7,
        [(13, 'Pi', False)] * 8,
    ]
    vypis_sloupecky(sloupecky)
    out, err = capsys.readouterr()
    check_text(out, """
        [???] [???] [???] [???] [???] [???] [???]
        [???] [???] [???] [???] [???] [???] [???]
              [???] [???] [???] [???] [???] [???]
                    [???] [???] [???] [???] [???]
                          [???] [???] [???] [???]
                                [???] [???] [???]
                                      [???] [???]
                                            [???]
    """)


@pytest.mark.level(42)
def test_vypis_sloupecky_zacatek_hry(capsys):
    """Kontrola výpisu sloupečků, kde jsou karty i rubem lícem nahoru"""
    from klondike import vypis_sloupecky
    sloupecky =  [
        [(13, 'Pi', False)] * 0 + [(8, 'Kr', True)],
        [(13, 'Pi', False)] * 1 + [(9, 'Ka', True)],
        [(13, 'Pi', False)] * 2 + [(10, 'Sr', True)],
        [(13, 'Pi', False)] * 3 + [(1, 'Ka', True)],
        [(13, 'Pi', False)] * 4 + [(4, 'Pi', True)],
        [(13, 'Pi', False)] * 5 + [(9, 'Kr', True)],
        [(13, 'Pi', False)] * 6 + [(12, 'Sr', True)],
    ]
    vypis_sloupecky(sloupecky)
    out, err = capsys.readouterr()
    check_text(out, """
        [8♣ ] [???] [???] [???] [???] [???] [???]
              [9 ♦] [???] [???] [???] [???] [???]
                    [X ♥] [???] [???] [???] [???]
                          [A ♦] [???] [???] [???]
                                [4♠ ] [???] [???]
                                      [9♣ ] [???]
                                            [Q ♥]
    """)


@pytest.mark.level(42)
def test_vypis_sloupecky_rozehrana(capsys):
    """Kontrola výpisu sloupečků rozehrané hry"""
    from klondike import vypis_sloupecky
    sloupecky = [
        [(13, 'Pi', False)] * 1 + [(8, 'Kr', True)],
        [(13, 'Pi', False)] * 8 + [(9, 'Ka', True)],
        [(13, 'Pi', False)] * 2 + [(10, 'Sr', True), (9, 'Kr', True), (8, 'Ka', True)],
        [(13, 'Pi', False)] * 6 + [(3, 'Ka', True)],
        [(13, 'Pi', False)] * 1 + [(4, 'Pi', True)],
        [(13, 'Pi', False)] * 9 + [(9, 'Kr', True)],
        [(13, 'Pi', False)] * 5 + [(12, 'Sr', True), (11, 'Pi', True)],
    ]
    vypis_sloupecky(sloupecky)
    out, err = capsys.readouterr()
    check_text(out, """
        [???] [???] [???] [???] [???] [???] [???]
        [8♣ ] [???] [???] [???] [4♠ ] [???] [???]
              [???] [X ♥] [???]       [???] [???]
              [???] [9♣ ] [???]       [???] [???]
              [???] [8 ♦] [???]       [???] [???]
              [???]       [???]       [???] [Q ♥]
              [???]       [3 ♦]       [???] [J♠ ]
              [???]                   [???]
              [9 ♦]                   [???]
                                      [9♣ ]
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


@pytest.mark.level(70)
def test_import_udelej_hru():
    from klondike import udelej_hru

@pytest.mark.level(71)
def test_udelej_hru_klice():
    """Hra by měl být slovník s klíči A až G a U až Z."""
    from klondike import udelej_hru
    hra = udelej_hru()
    assert sorted(hra) == list('ABCDEFGUVWXYZ')


@pytest.mark.level(71)
@pytest.mark.parametrize('pismenko', 'ABCDEFGUVWXYZ')
def test_pocty_karet(pismenko):
    """Počty karet v jednotlivých sloupcích jsou dané."""
    from klondike import udelej_hru
    hra = udelej_hru()

    POCTY = {
        'U': 24,
        'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0,
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7,
    }
    pozadovany_pocet = POCTY[pismenko]

    assert len(hra[pismenko]) == pozadovany_pocet


@pytest.mark.level(71)
def test_otoceni_karet_balicku():
    """Karty balíčku by měly být rubem nahoru"""
    from klondike import udelej_hru
    hra = udelej_hru()
    for hodnota, barva, licem_nahoru in hra['U']:
        assert not licem_nahoru


@pytest.mark.level(71)
@pytest.mark.parametrize('pismenko', 'ABCDEFG')
def test_otoceni_karet_sloupecku(pismenko):
    """Karty sloupečků by měly být rubem nahoru, kromě té poslední"""
    from klondike import udelej_hru
    hra = udelej_hru()
    sloupecek = hra[pismenko]

    # Poslední karta
    posledni_karta = sloupecek[-1]
    hodnota, barva, licem_nahoru = posledni_karta
    assert licem_nahoru

    # Ostatní karty
    for hodnota, barva, licem_nahoru in sloupecek[:-1]:
        assert not licem_nahoru


@pytest.mark.level(71)
def test_zamichani():
    """Každá hra by měla být jiná"""
    from klondike import udelej_hru
    hra1 = udelej_hru()
    hra2 = udelej_hru()

    # Je šance 1 z 80658175170943878571660636856403766975289505440883277824000000000000,
    # že dvě náhodné hry budou stejné.
    # Nejspíš je pravděpodobnější, že v průběhu testu odejde počítač,
    # na kterém test běží, než aby se ty karty zamíchaly stejně.
    assert hra1 != hra2, 'Karty nejsou zamíchané!'


@pytest.mark.level(71)
def test_vsech_karet():
    """Hra by měla obsahovat všech 52 karet, bez duplikátů."""
    from klondike import udelej_hru
    hra = udelej_hru()

    # Uděláme seznam dvojic (hodnota, barva), tedy karet s ignorovaným otočením
    dvojice_z_hry = []
    for balicek in hra.values():
        for hodnota, barva, licem_nahoru in balicek:
            dvojice_z_hry.append((hodnota, barva))
    # Seznam seřadíme -- na pořadí nezáleží
    dvojice_z_hry.sort()

    # Uděláme seznam dvojic (hodnota, barva) všech karet, kteŕe ve hře mají být
    pozadovane_dvojice = []
    for hodnota in range(1, 14):
        for barva in 'Ka', 'Kr', 'Pi', 'Sr':
            pozadovane_dvojice.append((hodnota, barva))
    # Tenhle seznam by měl být už seřazený, ale opatrnosti není nikdy dost
    pozadovane_dvojice.sort()

    # Ty dva seznamy (ten ze hry a ten z testu) by měly být stejné
    assert dvojice_z_hry == pozadovane_dvojice


@pytest.mark.level(80)
def test_import_vypis_hru():
    from klondike import vypis_hru

@pytest.mark.level(81)
def test_ruby(capsys):
    """Kontrola výpisu hry, kde jsou všechny karty rubem nahoru"""
    from klondike import udelej_hru, vypis_hru
    hra = udelej_hru()
    hra = {
        'U': [(13, 'Pi', False)],
        'V': [],
        'W': [],
        'X': [],
        'Y': [],
        'Z': [],
        'A': [(13, 'Pi', False)] * 2,
        'B': [(13, 'Pi', False)] * 3,
        'C': [(13, 'Pi', False)] * 4,
        'D': [(13, 'Pi', False)] * 5,
        'E': [(13, 'Pi', False)] * 6,
        'F': [(13, 'Pi', False)] * 7,
        'G': [(13, 'Pi', False)] * 8,
    }
    vypis_hru(hra)
    out, err = capsys.readouterr()
    check_text(out, """
          U     V           W     X     Y     Z
        [???] [   ]       [   ] [   ] [   ] [   ]

          A     B     C     D     E     F     G
        [???] [???] [???] [???] [???] [???] [???]
        [???] [???] [???] [???] [???] [???] [???]
              [???] [???] [???] [???] [???] [???]
                    [???] [???] [???] [???] [???]
                          [???] [???] [???] [???]
                                [???] [???] [???]
                                      [???] [???]
                                            [???]
    """)


@pytest.mark.level(81)
def test_zacatek_hry(capsys):
    """Kontrola výpisu hry, kde jsou karty i rubem lícem nahoru"""
    from klondike import vypis_hru
    hra = {
        'U': [(13, 'Pi', False)],
        'V': [(8, 'Kr', True), (13, 'Pi', True)],
        'W': [],
        'X': [],
        'Y': [],
        'Z': [],
        'A': [(13, 'Pi', False)] * 0 + [(8, 'Kr', True)],
        'B': [(13, 'Pi', False)] * 1 + [(9, 'Ka', True)],
        'C': [(13, 'Pi', False)] * 2 + [(10, 'Sr', True)],
        'D': [(13, 'Pi', False)] * 3 + [(1, 'Ka', True)],
        'E': [(13, 'Pi', False)] * 4 + [(4, 'Pi', True)],
        'F': [(13, 'Pi', False)] * 5 + [(9, 'Kr', True)],
        'G': [(13, 'Pi', False)] * 6 + [(12, 'Sr', True)],
    }
    vypis_hru(hra)
    out, err = capsys.readouterr()
    check_text(out, """
          U     V           W     X     Y     Z
        [???] [K♠ ]       [   ] [   ] [   ] [   ]

          A     B     C     D     E     F     G
        [8♣ ] [???] [???] [???] [???] [???] [???]
              [9 ♦] [???] [???] [???] [???] [???]
                    [X ♥] [???] [???] [???] [???]
                          [A ♦] [???] [???] [???]
                                [4♠ ] [???] [???]
                                      [9♣ ] [???]
                                            [Q ♥]
    """)


@pytest.mark.level(81)
def test_rozehrana(capsys):
    from klondike import vypis_hru
    """Kontrola výpisu rozehrané hry"""
    hra = {
        'U': [(13, 'Pi', False)],
        'V': [(8, 'Kr', True), (13, 'Pi', True)],
        'W': [(1, 'Pi', True)],
        'X': [(1, 'Kr', True)],
        'Y': [(1, 'Sr', True)],
        'Z': [(1, 'Ka', True), (2, 'Ka', True)],
        'A': [(13, 'Pi', False)] * 1 + [(8, 'Kr', True)],
        'B': [(13, 'Pi', False)] * 8 + [(9, 'Ka', True)],
        'C': [(13, 'Pi', False)] * 2 + [(10, 'Sr', True), (9, 'Kr', True), (8, 'Ka', True)],
        'D': [(13, 'Pi', False)] * 6 + [(3, 'Ka', True)],
        'E': [(13, 'Pi', False)] * 1 + [(4, 'Pi', True)],
        'F': [(13, 'Pi', False)] * 9 + [(9, 'Kr', True)],
        'G': [(13, 'Pi', False)] * 5 + [(12, 'Sr', True), (11, 'Pi', True)],
    }
    vypis_hru(hra)
    out, err = capsys.readouterr()
    check_text(out, """
          U     V           W     X     Y     Z
        [???] [K♠ ]       [A♠ ] [A♣ ] [A ♥] [2 ♦]

          A     B     C     D     E     F     G
        [???] [???] [???] [???] [???] [???] [???]
        [8♣ ] [???] [???] [???] [4♠ ] [???] [???]
              [???] [X ♥] [???]       [???] [???]
              [???] [9♣ ] [???]       [???] [???]
              [???] [8 ♦] [???]       [???] [???]
              [???]       [???]       [???] [Q ♥]
              [???]       [3 ♦]       [???] [J♠ ]
              [???]                   [???]
              [9 ♦]                   [???]
                                      [9♣ ]
    """)
