# Domácí projekty

Toto je složitější úkol, který ti zabere dost času a je potřeba ho pořádně projít.
Budou tu i pomocné informace, které nejsou zahrnuty v jiných materiálech.
Tak vzhůru do toho.

# Césarova šifra

Et tu?

César (ano, ten César) údajně používal k předávání tajných zpráv jednoduchou šifru. Posouval jednotlivé písmenka o několik pozic v abecedě. Například zapisoval A jako B, B jako C, C jako D, atd. až k Z jako A. Takže, kdyby chtěl poslat někomu anglický pozdrav, napsal by HELLO jako IFMMP. Příjemce takové zprávy musel znát "klíč" (v tomto případě číslo, o kolik se mají písmenka posunout), aby zprávu mohl dešifrovat a přečíst.

Tajemství tohoto systému záviselo na tom, že César a příjemci zprávy znali ono tajné číslo - počet míst v abacedě, o které se musí písmena ve zprávě posunout. Podle moderních standardů to není moc bezpečné, ale v jeho době to pochopitelně bylo terno.

Nezašifrovaný text se většinou jmenuje `plaintext`, zašifrovaný text `ciphertext` a tajné číslo `key`.

Aby to bylo opravdu jasné, ještě to znázorníme na příkladu HELLO (key 1) = IFMMP:

|  plaintext  |  H  |  E  |  L  |  L  |  O  |
| - | - | - | - | - | - |
|  + key  |  1  |  1  |  1  |  1  |  1  |
|  ciphertext  |  I  |  F  |  M  |  M  |  P  |

.

Více formálně, Césarova šifra "rotuje" každé písmeno o `k` pozic (k je `key`). Ještě více formálně, pokud `p` je plaintext (nezašifrovaný text), `pi` je í-tý znak v `p` a `k` je key (nezáporné celé číslo), tak každé písmeno `ci` v ciphertext `c` je počítáno jako

```bash
ci = (pi + k) % 26
```

Zápis % 26 je operátor `modulo` (vzpomínáš na operátory v Pythonu?) a znamená **zbytek po dělení 26**. Tato rovnice možná udělá ze šifry něco mnohem složitějšího, ale je to opravdu přesného vyjádření našeho algoritmu. (O tom, že vše je algoritmus jsme mluvili.)

Pojďme na psaní programu, který bude šifrovat jednoduchý text Césarovou šifrou.
Po spuštěníby se měl program zeptat, jaký klíč použít a jaký text zašifrovat. (Počítej s tím, že klíč má být pozitivní celé číslo)

Například:

```bash
$ python caesar.py
key: 1
plaintext:  HELLO
ciphertext: IFMMP
```

```bash
$ python caesar.py
key: 13
plaintext:  hello, world
ciphertext: uryyb, jbeyq
```

Všimni si, že se posunuly pouze písmena a ne mezery a další znaky.

Pokud uživatel nebude spolupracovat a bude psát věci, které nemá, měl by se ho program zeptat znovu. Například, když jako `key` zkusí zadat řetězec.

## Jak začít

Podívej se na některé záludnější věci, snad ti to pomůže s implementací.

### Pseudocode

Určitě je dobrá praxe pseudokód psát. Ukazovali jsme si ho na úplně první lekci (když jsme hledali jméno v telefonním seznamu). Je to jen logické uspořádání myšlenek, které pak přepíšeš pomocí Pythonu, aby tomu počítač rozumněl. Krátké věty nebo body jsou uplně dostačující.

### ASCII

Na první lekci jsi taky slyšela, že existuje ASCII tabulka. Je to konvence, kterou někdo dávno vymyslel, aby se znaky daly zapsat jako čísla. Vzpomínáš si na abstrakci?

Tady je odkaz na [ASCII](https://cs.wikipedia.org/wiki/ASCII). Bude důležité si to pročíst pro základní pochopení a zjištění, který znak má jakou hodnotu.

A jak se dostat ze znaku k číslu?

Python na to má fikanou funkci `ord`. Fungování nejlépe ilustruje příklad.

```python
>>> ord('a')
97
>>> chr(97)
'a'
>>> chr(ord('a') + 3)
'd'
>>>
```

Inverzní funkce od `ord` je `chr`

```python
>>> chr(97)
'a'
```

To je vše potřebné. V tomto úkolu neřeš znaky české abecedy (ani žádné jiné), protože by se to moc zkomplikovalo, a udělej jen šifru, která bude fungovat pro ASCII.

### A teď je řada na tobě

Už bylo zmíněno, že tento úkol bude vyžadovat větší úsílí. Nějaké samostudium, hodně práce a přemýšlení. Ale ten pocit, když ho dokončíš bude pozvnášející!
Kdyby ses přece jen zasekla, napiš koučovi.


# Návod na odevzdání domácího úkolu

* Přepni se na větev master `git checkout master`
* Vytvoř si novou větev, kterou si pojmenuj nějak unikátně (např. piskvorky). Je lepší nepoužívat diakritiku a jako oddělovač používat podtržítko. `git branch piskvorky`
* Přepni se do nové větve. `git checkout piskvorky`
* Napiš úkol.
* Přidej změny do stage a pak udělej commit. `git add piskvorky.py`,  `git commit -m 'Home work - game piskvorky.'`
* Pushni větev do repozitáře na githubu. `git push origin piskvorky`
* Udělej nový pull request. Návod v sekci Žádost o začlenění (pull request)
* Pošli koučovi odkaz na pull request do slacku.
* Potom, co ti kouč úkol schválí, udělej merge do master větve. Na stránce pull requestu v dolní části je zelené tlačíko `Merge pull request`. 
* Stáhni si změny do lokálního repozitáře (ve tvém počítači) do větve master. `git checkout master`, `git pull origin master`
* Pokud budeš v průběhu práce na domácích úkolu dělat změny v jiných souborech, přepni se nejdřív na větev master, udělej změny a commitni je a pak se vrať do větve s domácím úkolem.

# Bonusy

Interaktivní zábavný git [tutoriál](https://learngitbranching.js.org/).

Desktopová [aplikace](https://github.com/jlord/git-it-electron#what-to-install), která vás naučí používat Git (Jak ji nainstalovat je tam popsáno, kdybyste potřebovali pomoct, napište koučovi).

Kdyby měl někdo rád kočičky, tak tady je pár nákresů, jak funguje [git purr](https://girliemac.com/blog/2017/12/26/git-purr/).


A jedno video na vysvětlení [githubu](https://www.youtube.com/watch?v=w3jLJU7DT5E).