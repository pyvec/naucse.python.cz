import pytest
import klondike


def test_struktury():
    hra = klondike.udelej_hru()
    assert len(hra) == 3, 'Hra musí být trojice (balicky, hromadky, sloupecky)'

    balicky, hromadky, sloupecky = hra
    assert len(balicky) == 2
    assert len(hromadky) == 4
    assert len(sloupecky) == 7

    balicek_u, balicek_v = balicky
    assert len(balicek_u) == 24
    assert len(balicek_v) == 0

    for hodnota, barva, licem_nahoru in balicek_u:
        assert licem_nahoru == False

    for hromadka in hromadky:
        assert len(hromadka) == 0

    for index, sloupecek in enumerate(sloupecky):
        assert len(sloupecek) == index + 1

        for hodnota, barva, licem_nahoru in sloupecek[:-1]:
            assert licem_nahoru == False

        hodnota, barva, licem_nahoru = sloupecek[-1]
        assert licem_nahoru == True


def test_zamichani():
    hra1 = klondike.udelej_hru()
    hra2 = klondike.udelej_hru()

    # Je šance 1 z 80658175170943878571660636856403766975289505440883277824000000000000,
    # že dvě náhodné hry budou stejné.
    # Nejspíš je pravděpodobnější, že v průběhu testu odejde počítač,
    # na kterém test běží, než aby se ty karty zamíchaly stejně.
    assert hra1 != hra2, 'Karty nejsou zamíchané!'



def test_vsech_karet():
    hra = klondike.udelej_hru()
    dvojice = []
    for balicky in hra:
        for balicek in balicky:
            for hodnota, barva, licem_nahoru in balicek:
                dvojice.append((hodnota, barva))
    dvojice.sort()

    dvojice_exp = []
    for hodnota in range(1, 14):
        for barva in 'Ka', 'Kr', 'Pi', 'Sr':
            dvojice_exp.append((hodnota, barva))

    assert dvojice == dvojice_exp
