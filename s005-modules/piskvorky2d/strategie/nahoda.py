import random

def tah_pocitace(pole, symbol):
    if '-' not in pole:
        raise ValueError('Plné pole')
    while True:
        cislo = random.randrange(len(pole))
        if pole[cislo] == '-':
            return pole[:cislo] + symbol + pole[cislo+1:]
