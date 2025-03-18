"""Základní operace s "kartou" - trojicí (hodnota, barva, je_licem_nahoru)
"""

def popis_kartu(karta):
    """Vrátí popis karty, např. [Q ♥] nebo [6♣ ] nebo [???]

    Trojice čísla (2-13), krátkého řetězce ('Sr', 'Ka', 'Kr' nebo 'Pi')
    a logické hodnoty (True - lícem nahoru; False - rubem) se jednoduše
    zpracovává v Pythonu, ale pro "uživatele" není nic moc.
    Proto je tu tahle funkce, která kartu hezky "popíše".

    Aby měly všechny hodnoty jen jeden znak, desítka se vypisuje jako
    římská číslice "X".

    Aby se dalo rychle odlišit červené (♥♦) karty od černých (♣♠),
    mají červené mezeru před symbolem a černé za ním.
    """

    # Rozbalení n-tice, abychom mohli pracovat s jednotlivými složkami
    hodnota, barva, je_licem_nahoru = karta

    # Když je vidět jen rub, rovnou vrátíme [???]
    if not je_licem_nahoru:
        return '[???]'

    # Popis hodnoty: pár speciálních případů, plus čísla 2-9
    if hodnota == 11:
        popis_hodnoty = 'J'
    elif hodnota == 12:
        popis_hodnoty = 'Q'
    elif hodnota == 13:
        popis_hodnoty = 'K'
    elif hodnota == 1:
        popis_hodnoty = 'A'
    elif hodnota == 10:
        popis_hodnoty = 'X'
    else:
        popis_hodnoty = str(hodnota)

    # Popis barvy: čtyři možnosti
    if barva == 'Sr':
        popis_barvy = ' ♥'
    elif barva == 'Ka':
        popis_barvy = ' ♦'
    elif barva == 'Kr':
        popis_barvy = '♣ '
    elif barva == 'Pi':
        popis_barvy = '♠ '

    # Vrácení hodnoty
    return f'[{popis_hodnoty}{popis_barvy}]'


def otoc_kartu(karta, pozadovane_otoceni):
    """Vrátí kartu otočenou lícem nahoru (True) nebo rubem nahoru (False)

    Nemění původní trojici; vytvoří a vrátí novou.
    (Ani by to jinak nešlo – n-tice se, podobně jako řetězce čísla, měnit
    nedají.)
    """

    # Rozbalení n-tice
    hodnota, barva, stare_otoceni = karta

    # Vytvoření nové n-tice (kombinací staré hodnoty/barvy a nového otočení)
    nova_karta = hodnota, barva, pozadovane_otoceni

    # Vrácení nové n-tice
    return nova_karta
