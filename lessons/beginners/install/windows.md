# Instalace Pythonu pro Windows

Běž na [stahovací stránku Pythonu](https://www.python.org/downloads/)
a stáhni si instalátor nejnovější stabilní verze Pythonu.
Ověř si že je to verze **3.6.0 nebo novější** –
verze 3.6.0 má jistá vylepšení, která budeme v tomto kurzu používat.

Jak poznat, který instalátor je ten pravý?
Pokud má tvůj počítač 64bitovou verzi Windows,
stáhni si *Windows x86-64 executable installer*.
Pokud máš starší počítač s 32bitovými Windows,
stáhni si *Windows x86 executable installer*.
(Rozdíl je v *x86-64* versus *x86*.)

> [note]
> Kde zjistíš, zda máš 32bitové nebo 64bitové Windows? Otevři nabídku
> **Start**, vyhledat „Systém“ a otevřít **Systémové informace**.
> Pokud máš novější počítač, téměř jistě budeš mít Windows 64bitové.
>
> {{ figure(
    img=static('windows_32v64-bit.png'),
    alt='Screenshot zjišťování verze systému',
) }}

Stažený instalátor spusť.
Na začátku instalace zaškrtni **Install launcher for all users**
a také **Add Python to PATH**.
Tyto volby ti zjednoduší vytvoření virtuálního prostředí.

(Jestli nemáš administrátorské oprávnění, volbu
*Install launcher for all users* nezaškrtávej.)

{{ figure(
    img=static('windows_add_python_to_path.png'),
    alt='Screenshot instalace Pythonu',
) }}

Pak zmáčkni **Install now** a dále se drž instrukcí.

Máš-li otevřenou příkazovou řádku, po instalaci Pythonu ji zavři a otevři
novou.
Instalace mění systémové nastavení, které se musí načíst znovu.
