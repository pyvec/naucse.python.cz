argparse
========

Knihovna `argparse` je ve standardní knihovně a slouží k vytváření rozhraní pro příkazovou řádku
(angl. *command line interface*, CLI).

`argparse` toho neumí tolik jako [`click`]( {{ lesson_url('intro/click')}} ), ale pro spoustu
případů bohatě poslouží a každý s Pythonem ji má k dispozici bez nutnosti další instalace.

## Argumenty příkazové řádky

`argparse` není ve standardní knihovně jediným nástrojem na zpracování argumentů příkazové řádky.
Mezi jeho hlavní „konkurenty“ patří: [optparse] — předchůdce `argparse` — a [getopt].

[optparse]: https://docs.python.org/3/library/optparse.html
[getopt]: https://docs.python.org/3/library/getopt.html

A pro to úplně nejzákladnější zpracování argumentů nám stačí i modul `sys` a seznam `argv`:

```python
import sys

for index, argument in enumerate(sys.argv):
    print(f"Argument číslo {index} je: {argument}")
```

```console
$ python sys_module.py ahoj "ja jsem" argument
Argument číslo 0 je: sys_module.py
Argument číslo 1 je: ahoj
Argument číslo 2 je: ja jsem
Argument číslo 3 je: argument
```

`sys.argv` se hodí, pokud potřebujete získat z příkazové řádky třeba jen jeden argument
a program nepotřebuje nápovědu. Na složitější případy už je lepší použít `argparse`.

`argparse` nemá tak striktně definovanou strukturu jako `click`, takže se dá použít
více různými způsoby. Ten úplně nejzákladnější sestává z následujících kroků:

1. Vytvoříme si instanci třídy `ArgumentParser`.
2. Parseru přidáváme argumenty, které bude umět zpracovat.
3. Necháme parser zpracovat to, co nám přišlo z příkazové řádky.

```python
import argparse

def hello(name):
    print(f"Hello {name}!")

if __name__ == '__main__':
    # Vytvoříme prázdný parser
    parser = argparse.ArgumentParser(description='Sample app')
    # Naučíme ho zpracovávat první argument
    parser.add_argument("-n", "--name", action="store", dest="name", default="world")
    # Necháme jej zpracovat sys.argv
    arguments = parser.parse_args()
    # Spustíme funkci s argumentem z příkazové řádky
    hello(arguments.name)
```

Volání `parser.parse_args()` bez dalších informací zpracovává obsah seznamu `sys.argv`,
ale je i možné při testování zadat seznam argumentů ručně.

Pro každý argument je možné specifikovat celou řadu vlastností. V předchozím příkladu jsou první
dvě možná jména pro nový argument, následuje akce (`store` znamená ulož hodnotu), `dest` určuje,
jak se bude jmenovat atribut, kde bude uložená hodnota k dispozici a `default` nastavuje výchozí
hodnotu pro případ, kdy argument při spuštění skriptu vynecháme.

```console
$ python args.py
Hello world!
$ python args.py -n PyLadies
Hello PyLadies!
$ python args.py --name PyLadies 
Hello PyLadies!
$ python args.py --help         
usage: args.py [-h] [-n NAME]

Sample app

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME
```

Přepínač `--help` pro nápovědu získal náš program automaticky.

## Přepínače

Přepínače jsou v podstatě argumenty bez hodnoty a slouží k zapnutí nebo vypnutí
některé z vlastností programu. Například `--help` je také přepínač, který zobrazí nápovědu
a program ukončí, aniž by cokoli udělal.

Pro přepínače se používají akce `store_true` a `store_false`. `store_true` uloží
do proměnné `True`, pokud bude přepínač zadán na příkazové řádce, a naopak `store_false`
uloží `False` a hodí se tedy spíše pro vypnutí některé z vlastností.

```python
import argparse

def hello(name, upper, ex_mark):
    string = f"Hello {name}"
    if upper:
        string = string.upper()
    if ex_mark:
        string += "!"
    print(string)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample app')

    parser.add_argument("-n", "--name", action="store", dest="name", default="world")
    parser.add_argument("-u", "--uppercase", action="store_true", dest="upper")
    parser.add_argument("-E", "--no-exclamation-mark", action="store_false", dest="ex_mark")

    arguments = parser.parse_args()

    hello(arguments.name, arguments.upper, arguments.ex_mark)
```

Protože `store_true` má výchozí hodnotu `False` a opačně, definice argumentů výše
nám na chování programu bez jejich použití nic nezmění.

```console
$ python args.py -n PyLadies
Hello PyLadies!
```

Použijeme-li je, ovlivní nám podobu výstupu:

```console
$ python args.py -n PyLadies --upper
HELLO PYLADIES!
$ python args.py -n PyLadies --upper -E
HELLO PYLADIES
$ python args.py -E                    
Hello world
```

Výhodou parseru je, že můžeme argumenty použít v libovolném pořadí:

```console
$ python args.py -E --upper --name Ostrava
HELLO OSTRAVA
```

## Poziční argumenty

Stejně jako u funkcí mohou být i v příkazové řádce argumenty nepojmenované.
Používají se ve dvou případech: pro povinné parametry a pro parametry, kterých
může být zadán libovolný počet.
Na všechno ostatní radši použijte přepínače.

Například příkaz `cd` potřebuje jeden argument: jméno adresáře,
do kterého má přepnout.
Jeho rozhraní by mohlo vypadat takto:

```python
import argparse

def cd(dir):
    print(f"Changing to directory to {dir}!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample app')
    parser.add_argument("directory")
    arguments = parser.parse_args()

    cd(arguments.directory)
```

```console
$ python args.py                          
usage: args.py [-h] directory
args.py: error: the following arguments are required: directory
$ python args.py new_folder
Changing to directory new_folder
$ python args.py --help    
usage: args.py [-h] directory

Sample app

positional arguments:
  directory

optional arguments:
  -h, --help  show this help message and exit
```

Argument `directory` je poziční a povinný. Spuštění bez něj skončí chybou.
Za povšimnutí stojí, že nepovinné přepínače z minulých příkladů se v nápovědě
vždy zobrazovaly v hranatých závorkách.

Proměnný počet argumentů se zadává pomocí `nargs`. Možné hodnoty jsou:

* `N` — přesný počet vyjádřený číslem
* `?` — žádný nebo jeden argument
* `*` — libovolné množství argumentů včetně 0
* `+` — libovolné množství, ale minimálně jeden argument

Můžeme například nechat náš program pozdravit hned několikrát, ale minimálně jednou.

```python
import argparse

def hello(names, upper, ex_mark):
    for name in names:
        string = f"Hello {name}"
        if upper:
            string = string.upper()
        if ex_mark:
            string += "!"
        print(string)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample app')

    parser.add_argument("names", nargs="+")
    parser.add_argument("-u", "--uppercase", action="store_true", dest="upper")
    parser.add_argument("-E", "--no-exclamation-mark", action="store_false", dest="ex_mark")

    arguments = parser.parse_args()

    hello(arguments.names, arguments.upper, arguments.ex_mark)
```

Takový program už nebude možné spustit bez alespoň jednoho nepojmenovaného argumentu
a bude možné jich zadat hned několik. Tato skutečnost se zrcadlí i v nápovědě.

```console
$ python args.py       
usage: args.py [-h] [-u] [-E] names [names ...]
args.py: error: the following arguments are required: names

$ python args.py --help
usage: args.py [-h] [-u] [-E] names [names ...]

Sample app

positional arguments:
  names

optional arguments:
  -h, --help            show this help message and exit
  -u, --uppercase
  -E, --no-exclamation-mark

$ python args.py PyLadies Ostrava Pythonistas
Hello PyLadies!
Hello Ostrava!
Hello Pythonistas!
```

## Typy a validace

Prozatím všechny argumenty z příkazové řádky dostal náš program jako řetězce.
Toto chování lze jednoduše změnit nastavením `type`.

Například u jednoduchého dělení s dvěma povinnými argumenty se nám více
hodí mít oba jako desetinná čísla namísto řetězců.

```python
import argparse

def deleni(a, b):
    print(a / b)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample app')
    parser.add_argument("a", type=float)
    parser.add_argument("b", type=float)
    arguments = parser.parse_args()

    deleni(arguments.a, arguments.b)
```

```console
$ python deleni.py 10 5
2.0

$ python deleni.py 10 5.5
1.8181818181818181
```

`type` bere jakoukoli funkci, kterou pak řetězec s hodnotou argumentu prožene
a uloží si výsledek. Takže nejen `int`, `bool` a `float`, ale i libovolná vlastní funkce
zde může sloužit nejen pro změnu typu argumentu ale třeba také pro jeho validaci nebo libovolné
další úpravy.

```python
import argparse

def validate_email(address):
    if "@" not in address:
        raise argparse.ArgumentTypeError("Missing @ in email address")
    if not address.endswith("@python.cz"):
        raise argparse.ArgumentTypeError("Recipient address not from our domain")
    return address

def send_email(address):
    print(f"Sending email to {address}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample app')
    parser.add_argument("address", type=validate_email)
    arguments = parser.parse_args()

    send_email(arguments.address)
```

```console
$ python email.py tomas  
usage: email.py [-h] address
email.py: error: argument address: Missing @ in email address

$ python email.py tomas@gmail.com
usage: email.py [-h] address
email.py: error: argument address: Recipient address not from out domain

$ python email.py tomas@python.cz
Sending email to tomas@python.cz
```

Jako bonus způsobí vyvolání výjimky `ArgumentTypeError` automatické zobrazení nápovědy.

## Soubory

Speciálním typem argumentu jsou cesty k souborům. Je samozřejmě možné
je zpracovávat jako řetězce, ale není to nejlepší nápad a je to zbytečně pracné.

`argparse` má pro tyto účely speciální `FileType`, který nám soubor také rovnou otevře.

```python
import argparse

def row_count(file):
    n = len(file.read().splitlines())
    print(f"Row count: {n}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample app')
    parser.add_argument("file", type=argparse.FileType(mode="r"))
    arguments = parser.parse_args()

    row_count(arguments.file)
```

```console
$ python soubor.py          
usage: soubor.py [-h] file
soubor.py: error: the following arguments are required: file

$ python soubor.py deleni.py
Row count: 13

$ python soubor.py args.py   
Row count: 12

$ python soubor.py neexistujici
usage: soubor.py [-h] file
soubor.py: error: argument file: can't open 'neexistujici': [Errno 2] No such file or directory: 'neexistujici'
```

## A další

Nejedná se o vyčerpávající popis možností modulu `argparse`, ale spíše ukázku.
Vše ostatní je jako obvykle dostupné v [dokumentaci].

Jak je vidět, i se standardní knihovnou si v mnoha případech vystačíme.
O důvod více dobře zvážit, zda jsou externí závislosti opravdu potřeba.

[dokumentaci]: https://docs.python.org/3/library/argparse.html
