import klondike


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



def test_tahy():
    """Simuluje hru, jednak pomocí udelej_tah a jednak manipulací seznamů,
    a zkouší jestli všechno sedí."""
    hra_h = udelej_vzorovou_hru()
    hra_v = udelej_vzorovou_hru()
    balicky_h, hromadky_h, sloupecky_h = hra_h
    balicky_v, hromadky_v, sloupecky_v = hra_v
    klondike.vypis_hru(hra_h)

    # 7 na 8
    klondike.udelej_tah(hra_h, (sloupecky_h[0], 1, sloupecky_h[3]))
    sloupecky_v[0].pop()
    sloupecky_v[3].append((7, 'Pi', True))
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # (7, 8) na 9
    klondike.udelej_tah(hra_h, (sloupecky_h[3], 2, sloupecky_h[2]))
    sloupecky_v[3][-3:] = [(5, 'Kr', True)]
    sloupecky_v[2].extend([(8, 'Ka', True), (7, 'Pi', True)])
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # Otočení karty z balíčku
    klondike.udelej_tah(hra_h, 'U')
    balicky_v[0].pop()
    balicky_v[1].append((5, 'Sr', True))
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # Otočení karty z balíčku (7×)
    for i in range(7):
        klondike.udelej_tah(hra_h, 'U')
    del balicky_v[0][-7:]
    balicky_v[1].extend([
        (11, 'Ka', True),
        (3, 'Kr', True),
        (10, 'Kr', True),
        (12, 'Pi', True),
        (9, 'Ka', True),
        (8, 'Sr', True),
        (13, 'Kr', True),
    ])
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # Král na volné místo
    klondike.udelej_tah(hra_h, (balicky_h[1], 1, sloupecky_h[0]))
    balicky_v[1].pop()
    sloupecky_v[0].append((13, 'Kr', True))
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # Otočení karty z balíčku (5×)
    for i in range(5):
        klondike.udelej_tah(hra_h, 'U')
    del balicky_v[0][-5:]
    balicky_v[1].extend([
        (4, 'Ka', True),
        (6, 'Pi', True),
        (9, 'Kr', True),
        (2, 'Pi', True),
        (1, 'Pi', True),
    ])
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # Eso na cíl
    klondike.udelej_tah(hra_h, (balicky_h[1], 1, hromadky_h[2]))
    balicky_v[1].pop()
    hromadky_v[2].append((1, 'Pi', True))
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # Dvojka na cíl
    klondike.udelej_tah(hra_h, (balicky_h[1], 1, hromadky_h[2]))
    balicky_v[1].pop()
    hromadky_v[2].append((2, 'Pi', True))
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v

    # Otočení karty z balíčku (10×) + otočení balíčku
    for i in range(12):
        klondike.udelej_tah(hra_h, 'U')
    balicky_v[1].clear()
    balicky_v[0][:] = udelej_vzorovou_hru()[0][0]
    del balicky_v[0][16]  # král
    del balicky_v[0][11]  # eso
    del balicky_v[0][11]  # dvojka
    klondike.vypis_hru(hra_h)
    assert hra_h == hra_v
