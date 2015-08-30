import klondike

import random; random.seed(0)

hra = klondike.udelej_hru()
klondike.vypis_hru(hra)
while not klondike.hrac_vyhral(hra):
    tah = klondike.nacti_tah()
    try:
        info = klondike.priprav_tah(hra, tah)
    except ValueError as e:
        print(e)
    else:
        klondike.udelej_tah(hra, info)
        klondike.vypis_hru(hra)
