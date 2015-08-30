import klondike
import textwrap
import re

ASCII_ONLY = False

def check(got, expected):
    if ASCII_ONLY:
        expected = expected.replace('♠', 'P')
        expected = expected.replace('♥', 'S')
        expected = expected.replace('♦', 'K')
        expected = expected.replace('♣', '+')
    got = re.sub(' +\n', '\n', got)  # odstraní mezery z konců řádků
    print(got)
    assert got.strip() == textwrap.dedent(expected).strip()



# I `print` jde testovat, dělá se to pomocí "capsys":
def test_ruby(capsys):
    balicky = [(13, 'Pi', False)], []
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
    klondike.vypis_hru(hra)
    out, err = capsys.readouterr()
    check(out, """
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


def test_lice(capsys):
    balicky = [(13, 'Pi', False)], [(8, 'Kr', True), (13, 'Pi', True)]
    hromadky = [], [], [], []
    sloupecky = (
        [(13, 'Pi', False)] * 1 + [(8, 'Kr', True)],
        [(13, 'Pi', False)] * 2 + [(9, 'Ka', True)],
        [(13, 'Pi', False)] * 3 + [(10, 'Sr', True)],
        [(13, 'Pi', False)] * 4 + [(1, 'Ka', True)],
        [(13, 'Pi', False)] * 5 + [(4, 'Pi', True)],
        [(13, 'Pi', False)] * 6 + [(9, 'Kr', True)],
        [(13, 'Pi', False)] * 7 + [(12, 'Sr', True)],
    )
    hra = balicky, hromadky, sloupecky
    klondike.vypis_hru(hra)
    out, err = capsys.readouterr()
    check(out, """
          U     V           W     X     Y     Z
        [???] [K♠ ]       [   ] [   ] [   ] [   ]

          A     B     C     D     E     F     G
        [???] [???] [???] [???] [???] [???] [???]
        [8♣ ] [???] [???] [???] [???] [???] [???]
              [9 ♦] [???] [???] [???] [???] [???]
                    [X ♥] [???] [???] [???] [???]
                          [A ♦] [???] [???] [???]
                                [4♠ ] [???] [???]
                                      [9♣ ] [???]
                                            [Q ♥]
    """)


def test_rozehrana(capsys):
    balicky = [(13, 'Pi', False)], [(8, 'Kr', True), (13, 'Pi', True)]
    hromadky = (
        [(1, 'Pi', True)],
        [(1, 'Kr', True)],
        [(1, 'Sr', True)],
        [(1, 'Ka', True), (2, 'Ka', True)],
    )
    sloupecky = (
        [(13, 'Pi', False)] * 1 + [(8, 'Kr', True)],
        [(13, 'Pi', False)] * 8 + [(9, 'Ka', True)],
        [(13, 'Pi', False)] * 2 + [(10, 'Sr', True), (9, 'Kr', True), (8, 'Ka', True)],
        [(13, 'Pi', False)] * 6 + [(3, 'Ka', True)],
        [(13, 'Pi', False)] * 1 + [(4, 'Pi', True)],
        [(13, 'Pi', False)] * 9 + [(9, 'Kr', True)],
        [(13, 'Pi', False)] * 5 + [(12, 'Sr', True), (11, 'Pi', True)],
    )
    hra = balicky, hromadky, sloupecky
    klondike.vypis_hru(hra)
    out, err = capsys.readouterr()
    check(out, """
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
