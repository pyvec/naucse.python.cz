import klondike

def test_nevyhral_na_zacatku():
    hra = klondike.udelej_hru()
    assert not klondike.hrac_vyhral(hra)


def test_nevyhral_prazdny_balicek():
    balicky = [], []
    hromadky = [], [], [], []
    sloupecky = (
        [(13, 'Pi', False)] * 2,
        [(13, 'Pi', False)] * 3,
        [(13, 'Pi', False)] * 4,
        [(13, 'Pi', False)] * 5,
        [(13, 'Pi', False)] * 6,
        [(13, 'Pi', False)] * 7,
        [(13, 'Pi', False)] * 8,
    )
    hra = balicky, hromadky, sloupecky
    assert not klondike.hrac_vyhral(hra)


def test_nevyhral_prazdne_sloupecky():
    balicky = [(13, 'Pi', False)], []
    hromadky = [], [], [], []
    sloupecky = [], [], [], [], [], [], []
    hra = balicky, hromadky, sloupecky
    assert not klondike.hrac_vyhral(hra)


def test_vyhral():
    balicky = [], []
    hromadky = ([(n, 'Pi', True) for n in range(1, 14)],
                [(n, 'Sr', True) for n in range(1, 14)],
                [(n, 'Ka', True) for n in range(1, 14)],
                [(n, 'Kr', True) for n in range(1, 14)])
    sloupecky = [], [], [], [], [], [], []
    hra = balicky, hromadky, sloupecky
    assert klondike.hrac_vyhral(hra)
