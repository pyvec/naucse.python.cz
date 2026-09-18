"""Modul s funkcemi pro okýnkové otázky a odpovědi:

input(otazka) -> str

nacti_cislo(otazka) -> int

ano_nebo_ne(otazka) -> bool

print(argument0, argument1, argument2, ..., argument_n, sep='')

"""

from tkinter import Tk, LEFT, RIGHT, BOTTOM, TOP, W
from tkinter.ttk import Label, Button, Entry

# Spinbox byl přidán v Pythonu 3.7
try:
    from tkinter.ttk import Spinbox
except ImportError:
    Spinbox = None


# Následující kód používá několik pokročilejších technik.
# Není důležité *jak* je kód napsaný, ale že je možné ho napsat – a že daná
# funkce má dané rozhraní :)
#
# Mimochodem; opravdové funkce input a print jsou ještě složitější; viz:
#  https://github.com/python/cpython/blob/ce105541f/Python/bltinmodule.c#L1931
#  https://github.com/python/cpython/blob/ce105541f/Python/bltinmodule.c#L1827

# Funkce používají modul tkinter, který je zabudovaný v Pythonu, ale okýnka
# s ním vytvořená nevypadají příliš profesionálně.
# Budeš-li chtít začít psát "okýnkové" programy, doporučuji začít rovnou
# s knihovnou jako Qt nebo GTK.
# Na Qt máme mimochodem lekci v pokročilém kurzu, viz:
#    https://naucse.python.cz/course/mi-pyt/intro/pyqt/


def input(otazka='odpověz'):
    """Zeptá se uživatele na otázku a vrátí odpověď jako řetězec."""
    root = Tk()
    root.title(otazka)

    button = Button(root, text="OK", command=root.quit)
    button.pack(side=RIGHT)

    entry = Entry(root)
    entry.pack(side=LEFT)

    root.mainloop()

    value = entry.get()
    root.destroy()

    return value


def nacti_cislo(otazka='Zadej číslo'):
    """Zeptá se uživatele na otázku a vrátí odpověď jako celé číslo."""
    if Spinbox == None:
        raise NotImplementedError(
            "nacti_cislo bohužel potřebuje Python verze 3.7 a výš"
        )

    root = Tk()
    root.title(otazka)

    entry = Spinbox(root, from_=0, to=100)
    entry.set('0')
    entry.pack(side=LEFT)

    # Předbíháme: vnořená funkce může přistupovat
    # k proměnným "entry" a "root", které jsou
    # lokální pro "vnější" funkci (nacti_cislo)

    def ok_pressed():
        text = entry.get()
        try:
            value = int(text)
        except ValueError:
            entry.set('sem zadej číslo!')
        else:
            root.quit()

    button = Button(root, text="OK", command=ok_pressed)
    button.pack(side=RIGHT)

    root.mainloop()

    value = int(entry.get())
    root.destroy()

    return value


def ano_nebo_ne(otazka='Ano nebo ne?'):
    """Dá uživateli na výběr Ano/Ne a vrátí odpověď True nebo False."""
    root = Tk()
    root.title("Ano nebo ne?")

    value = False

    # Předbíháme: "nonlocal" umožňuje *měnit*
    # lokální proměnnou z vnější funkce.
    # (A definujeme tady funkci v rámci jiné funkce, takže problematika
    # lokálních proměnných je tu ještě složitější než na kurzu.)

    def yes():
        nonlocal value
        value = True
        root.quit()

    def no():
        nonlocal value
        value = False
        root.quit()

    label = Label(root, text=otazka)
    label.pack(side=TOP, expand=True, padx=20, pady=10)

    button = Button(root, text="Ano", command=yes)
    button.pack(side=LEFT, expand=True, padx=10, pady=10)

    button = Button(root, text="Ne", command=no)
    button.pack(side=RIGHT, expand=True, padx=10, pady=10)

    root.mainloop()
    root.destroy()

    return value



# Předbíháme: hvězdička v *args umožní že "print" bere proměnný
# počet argumentů; přes "args" se potom dá projít příkazem "for"
def print(*args, sep=' ', end='', file=None, flush=False):
    """Zobrazí dané argumenty."""
    root = Tk()
    root.title('print')

    str_args = ''
    for arg in args:
        str_args = str_args + sep + str(arg)

    label = Label(root, text=str_args[len(sep):] + end)
    label.pack(anchor=W)

    button = Button(root, text="OK", command=root.quit)
    button.pack(side=BOTTOM)

    root.bind('<Return>', (lambda e: root.quit()))
    root.mainloop()
    root.destroy()


# A tady je trik, jak kousek kódu nespustit když se modul importuje.
# Pro opravdové programy ale doporučuji spouštěcí modul, viz kurz.
if __name__ == '__main__':
    print(input())
    print(ano_nebo_ne())
    print('a', 'b', 'c', sep='; ', end='-')
    print(nacti_cislo())
