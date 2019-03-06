# 1D piškvorky s testy #

## Co to je? ##

Poté, co ses naučila pracovat s [řetězci][str] a psát [vlastní funkce][def], dostala jsi za [úkol][handout5] naprogramovat si jednoduchou hru: jednorozměrné piškvorky. V domácím projektu je předepsáno, z jakých dílčích funkcí se bude hra skládat. Mrkni se na zadání domácího projektu, než budeš pokračovat. Detailního popisu zadání hned využijeme a nahlédneme do pokročilejší lekce – té o [testování][testing]. Lekci o testování není třeba studovat celou, na to se podíváme společně za několik lekcí, ale můžeš v ní najít odpovědi na některé otázky.

Testování ti pomůže ověřit, že tvůj program funguje, jak má. Neboj se však nic, všechno to složitější jsme zatím napsali za tebe. Ty tak můžeš postupovat podle zadání domácích projektů a testy ti spuštěním jednoho jednoduchého příkazu ukážou, jak moc blízko jsi dokončení programu.

Toto je bonusový materiál, který může udělat domácí úkol zajímavější a naučit tě při tom opět něco nového. Pokud máš ale plné ruce práce se zvládáním aktuální látky, klidně postupuj jen podle zadání domácích projektů a na testování se společně podíváme později.

## Jak na to? ##

1. Stáhni si připravený soubor pro [piškvorky][piskvorky] a [soubor s testy][testpiskvorky] a ulož je do samostatné složky.

    V souboru *test_piskvorky.py* máš připravené testy. Nic v něm neměň, ale můžeš se do něj podívat. Samotnou hru pak piš do připraveného souboru _piskvorky.py_. Máš tam nachystané všechny potřebné funkce, jen zatím nic nedělají. Až je všechny doplníš, budeš mít funkční hru.

1. Aktivuj si své virtuální prostředí. Jak na to jsme si ukázali [na začátku kurzu][venvsetup].
1. Nainstaluj si knihovnu [pytest] podle [návodu][testing] v materiálech. Právě ta ti umožní ověřit správnou funkčnost programu.

    ```shell
    (venv) $ pip install pytest
    ```

1. Opět podle návodu pytest spusť.

    ```shell
    (venv) $ pytest -v test_piskvorky.py
    ```

## Co s tím? ##

Pytest ti vypíše, kde všude v tvém programu narazil na problém. Tyto jsou podrobně rozepsané a výstup je tak trochu dlouhý. Na jeho začátku však budeš mít takovéto řádky:

```
test_piskvorky.py::test_vyhodnot_vyhra_x FAILED
test_piskvorky.py::test_vyhodnot_vyhra_o FAILED
test_piskvorky.py::test_vyhodnot_remiza FAILED
…
test_piskvorky.py::test_tah_pocitace_skoro_plne_konec_2 FAILED
```

Každé _FAILED_ znamená jednu chybu: jeden test, který neprošel. Protože jsi zatím nic nenapsala, je problém úplně ve všem. To se ale změní, jakmile splníš první úkol: zařídíš, aby funkce _vyhodnot_ rozpoznala, že vyhrál hráč s křížky.

```
test_piskvorky.py::test_vyhodnot_vyhra_x PASSED
test_piskvorky.py::test_vyhodnot_vyhra_o FAILED
test_piskvorky.py::test_vyhodnot_remiza FAILED
…
test_piskvorky.py::test_tah_pocitace_skoro_plne_konec_2 FAILED
```

Vidíš? Výsledek prvního testu se změnil na _PASSED_. To znamená, že v tomto případě program funguje, jak má.

Až budeš mít program hotový, místo všech červených _FAILED_ bude u všech testů zelené _PASSED_. Pak víš, že máš hotovo. Teda, skoro.

```
test_piskvorky.py::test_vyhodnot_vyhra_x PASSED
test_piskvorky.py::test_vyhodnot_vyhra_o PASSED
…
test_piskvorky.py::test_tah_pocitace_skoro_plne_konec PASSED
test_piskvorky.py::test_tah_pocitace_skoro_plne_konec_2 PASSED
```

Proč jen skoro? Některé věci testovat moc dobře nejdou, nebo by to bylo pro tebe v tuto chvíli moc složité.

* Jednou takovou věcí je zadání od uživatele. Funkci *tah_hrace* proto pytest netestuje. To pak platí i pro celé jádro hry, funkci _piskvorky1d_, která právě funkci *tah_hrace* používá, když je hráč na tahu.
* Druhou věcí, která není testy pokryta, je vypisování na obrazovku. Tedy všechna zvolání o chybách či stavu hry.

Tyto věci musíš ověřit ručně. To by ale nemuselo být tak hrozné: programuješ hru a testováním si rovnou i hraješ.

## Co dál? ##

Snad ti tato zkušenost ukázala, že automatické testování ti může ušetřit čas a práci. Že díky testům si můžeš být jistá, že jsi úpravou programu nerozbila nic, co před tím fungovalo.

Nahlédni do souboru *test_piskvorky.py*. Možná teď ještě nebudeš rozumět do detailu, jak to všechno vlastně funguje, ale i tak uvidíš, že to není raketová věda. Máš herní pole v nějakém stavu, zavoláš svou funkci, a ověříš, že vrátila to, co by měla.

```python
assert tah("--------------------", 10, "x") == "----------x---------"
```

[Později][testing] se naučíš psát si testy sama. Snad ti tenhle malý exkurs ukázal, proč to není zbytečnost a že se ta trocha přidané námahy na začátku skutečně vyplatí.

[str]: {{ lesson_url('beginners/str') }}
[def]: {{ lesson_url('beginners/def') }}
[handout5]: {{ lesson_url('homework/ostrava5') }}
[testing]: {{ lesson_url('beginners/testing') }}
[venvsetup]: {{ lesson_url('beginners/venv-setup') }}
[pytest]: https://pytest.readthedocs.io/
[testpiskvorky]: static/test_piskvorky.py
[piskvorky]: static/piskvorky.py
