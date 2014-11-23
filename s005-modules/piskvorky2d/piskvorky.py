def tah(pole, index, symbol):
    if pole[index] != '-':
        raise ValueError('Pole {} je obsazeno symbolem {}'.format(index, pole[index]))
    return pole[:index] + symbol + pole[index + 1:]
