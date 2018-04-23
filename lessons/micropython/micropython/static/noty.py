nazvy = 'A', 'A#', 'H', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'

for i in range(88):
    frekvence = 27.5 * 2.**(i/12.)
    oktava = (i+9) // 12
    nota = '{:2} {}'.format(nazvy[i%12], oktava)
    if __name__ == '__main__':
        print("{}: {:7.2f}".format(nota, frekvence))
