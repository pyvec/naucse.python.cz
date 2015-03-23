class Karta:
    def __init__(self, hodnota, barva, licem_nahoru):
        self.hodnota = hodnota
        self.barva = barva
        self.licem_nahoru = licem_nahoru

    def __str__(self):
        if not self.licem_nahoru:
            return '[???]'

        barvy = {'Pi': '♠ ', 'Sr': ' ♥', 'Ka': ' ♦', 'Kr':'♣ '}
        znak_barvy = barvy[self.barva]

        hodnoty = {1: 'A', 10: 'X', 11: 'J', 12: 'Q', 13: 'K'}
        znak_hodnoty = hodnoty.get(self.hodnota, str(self.hodnota))

        return '[{}{}]'.format(znak_hodnoty, znak_barvy)

    def otoc_licem_nahoru(self):
        self.licem_nahoru = True

    def otoc_licem_dolu(self):
        self.licem_nahoru = False


karta = Karta(3, 'Sr', licem_nahoru=True)
print(karta.hodnota)        # → 3
print(karta.barva)          # → 'Sr'
print(karta.licem_nahoru)   # → True
print(karta)                # → [3 ♥]
karta.otoc_licem_dolu()
print(karta)                # → [???]
karta.otoc_licem_nahoru()
print(karta)                # → [3 ♥]
