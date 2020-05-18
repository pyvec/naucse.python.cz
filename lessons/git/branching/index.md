# Větvení v Gitu

Takže, Git už znáš!
Teď to začne být trošičku složitější :)

Programáto{{ gnd('ři', 'rky', both='ři') }} občas potřebují pracovat na dvou
věcech zároveň.
V projektu do práce se objeví se chyba,
která musí být opravená
ještě dnes, tak programátor{{ gnd('', 'ka') }} opustí, co zrovna dělá,
vrátí se k nějaké „stabilní” verzi, opraví chybu
a odešle ji zákazníkům.
A pak se vrátí k tomu, co dělal{{a}} předtím – jen ještě
musí zakomponovat opravu chyby i do verze, na které
pracuje dlouhodobě.

Git na to má takzvané *větve* (angl. *branches*).
Na jedné „větvi” se pracuje, ale je možné se přepnout do
jiné (třeba starší) větve, udělat pár změn
a pak se zase přepnout do nové větve a
pokračovat dál nebo sloučit změny.

Větvení využijeme i při spolupráci více lidí – každý
dělá na vlastní větvi a když přijde čas,
tak se různé změny sloučí dohromady.

Podívej se, jaké máš větve ve svém repozitáři.
K tomu slouží příkaz `git branch`:

```ansi
␛[36m$␛[0m git branch
* ␛[32mmaster␛[m
```

Je tam jenom jedna a jmenuje se `master`
– to je tradičně jméno „hlavní” větve.

K vytvoření nové větve znovu použiješ
`git branch`, jen tomu příkazu dáš navíc
jméno nové větve.
Třeba budeš chtít k básničce doplnit jméno autora,
tak větev pojmenuješ `doplneni-autora`.

```ansi
␛[36m$␛[0m git branch doplneni-autora
␛[36m$␛[0m git branch
  doplneni-autora␛[m
* ␛[32mmaster␛[m
```

Tenhle příkaz sice udělal novou větev,
ale nepřepnul do ní.
Hvězdička ve výstupu z `git branch` ukazuje,
že stále pracuješ v `master`.
Na přepnutí budeš potřebovat další příkaz:

```ansi
␛[36m$␛[0m git checkout doplneni-autora
Switched to branch 'doplneni-autora'
␛[36m$␛[0m git branch
* ␛[32mdoplneni-autora␛[m
  master␛[m
```

Tak. Teď jsi „ve” větvi `doplneni-autora`.
Doplň nějaké jméno na začátek souboru `basnicka.txt`,
a pomocí `git add` a `git commit` udělej novou revizi.
Pak koukni na `gitk --all`, jak to vypadá:

{{ figure(
    img=static('branch1.png'),
    alt="Výstup programu `gitk` s větví doplneni-autora",
) }}

Aktuální větev – `doplneni-autora` – je
zvýrazněná tučně a starší `master` je stále
na původní revizi.

Opusťme teď na chvíli práci na doplňování autora.
Vrať se do větve `master` a vytvoř z ní
větev `doplneni-jmena`.
Pak se na tuhle novou větev přepni.

```ansi
␛[36m$␛[0m git checkout master
Switched to branch 'master'
␛[36m$␛[0m git branch doplneni-jmena
␛[36m$␛[0m git checkout doplneni-jmena
Switched to branch 'doplneni-jmena'
␛[36m$␛[0m git branch
  doplneni-autora␛[m
* ␛[32mdoplneni-jmena␛[m
  master␛[m
```

Doplň jméno básně na začátek souboru (tedy na stejné místo,
jako je v druhé větvi název) a pomocí
`git add`, `git commit` ulož revizi.
Všechno zkontroluj přes `gitk --all`.

{{ figure(
    img=static('branches.png'),
    alt="Výstup programu `gitk` s větvemi doplneni-autora a doplneni-nazvu",
) }}


Takhle nějak se dá postupovat v situaci popsané v úvodu:
opuštění rozpracované verze, přechod na „stabilní”
verzi `master` a začátek práce v jiné
části projektu.

Mezi jednotlivými větvemi se dá podle libosti přepínat,
jen je vždycky dobré před přepnutím udělat novou revizi
(`git commit`) a pomocí `git status` zkontrolovat, jestli je všechno
uložené v Gitu.

Na stejném principu funguje i spolupráce několika lidí
na jednom projektu: je nějaký společný základ
(`master`) a každý dělá na vlastní větvi, dokud není se svými změnami spokojený.

A až je některá větev hotová, může se začlenit
zpátky do `master`. Podívejme se jak na to.


## Sloučení

Nedávalo by smysl historii projektu rozdvojovat,
kdyby pak jednotlivé větve nešly zase sloučit dohromady.
V Gitu je většinou slučování poměrně jednoduché, ale tento příklad schválně
ukazuje nejsložitější variantu, která může nastat.

Přepni se zpátky na `master`
a použij příkaz `git merge`, který
sloučí jinou větev s tou aktuální.
Příkazu musíš dát jméno větve, kterou chceš sloučit.

```ansi
␛[36m$␛[0m git checkout master
Switched to branch 'master'
␛[36m$␛[0m git merge doplneni-jmena
Updating 1fcd654..5c9bf93
Fast-forward
 basnicka.txt | 3 ␛[32m+++␛[m
 1 file changed, 3 insertions(+)
```

Sloučeno! Ono „`Fast-forward`” znamená, že
vlastně nebylo co slučovat – jen se do větve
`master` přidaly nové změny.
Zkontroluj v `gitk --all`, jak to vypadá.

A pak zkus sloučit i druhou větev: `git merge doplneni-autora`.
Tady to bude složitější: pravděpodobně se stane, že změny nepůjdou
automaticky sloučit a ve výstupu se objeví hláška
`merge conflict` (slučovací konflikt):

```ansi
␛[36m$␛[0m git merge doplneni-autora
Auto-merging basnicka.txt
CONFLICT (content): Merge conflict in basnicka.txt
Automatic merge failed; fix conflicts and then commit the result.
```

> [note] A když ne?
> Jestli se konflikt neobjevil, Git změny sloučil sám.
> Gratuluji! Zbytek téhle sekce bude jen teoretický; vrať se sem, až se ti
> někdy „podaří“ konflikt udělat.

Když nastane konflikt, `git status` ukáže „both modified“ – tedy že byl soubor
změněný v obou slučovaných větvích:

```ansi
␛[36m$␛[0m git status
On branch master
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	␛[31mboth modified:   basnicka.txt␛[m

no changes added to commit (use "git add" and/or "git commit -a")
```
V tom případě se na soubor podívej v editoru: objeví
se v něm obsah z obou konfliktních verzí,
společně se značkami `<<<<<<<`, `=======` a `>>>>>>>`, které upozorňují na
místo kde konflikt nastal.

Značky ukáže i příkaz `git diff`, jehož výstup je teď trošku složitější:

```ansi
␛[36m$␛[0m git diff
␛[1mdiff --cc basnicka.txt␛[m
␛[1mindex bc7a2de,88e7ea5..0000000␛[m
␛[1m--- a/basnicka.txt␛[m
␛[1m+++ b/basnicka.txt␛[m
␛[36m@@@ -1,4 -1,4 +1,8 @@@␛[m
␛[32m++<<<<<<< HEAD␛[m
␛[32m +Holka Modrooká␛[m
␛[32m++=======␛[m
␛[32m+ (Lidová)␛[m
␛[32m++>>>>>>> doplneni-autora␛[m
  ␛[m
  Holka modrooká␛[m
  Nesedávej u potoka␛[m
```

Konflikty a značky, které můžou být nepřehledné, ukazuje Git ze stejného důvodu
jako Python chybové hlášky: tedy aby ti co nejvíce pomohl.
Git je jen „hloupý“ nástroj a s konfliktem si neporadí sám, ale snaží se
ti řešení konfliktu co nejvíc usnadnit.

Proto hlavně nepanikař!
Soubor otevři v editoru a uprav **tak, jak by měl vypadat**.
Značky jako `<<<<<<<` smaž; řádky poskládej tak, jak by měly jít za sebou.
(A pracuješ-li na kódu, spusť testy a ověř, jestli všechno stále funguje.)

Pak soubor ulož a zadej `git commit`.
 
Ať nastal konflikt nebo ne, vytvoří se „slučovací revize“
(angl. *merge commit*), které – jako každé revizi – můžeš dát popisek.
Tentokrát je popisek už předvyplněný; chceš-li nějaký jiný, nahraď ho.

```ansi
␛[36m$␛[0m git add basnicka.txt
␛[36m$␛[0m git commit
[master 884b30a] Merge branch 'doplneni-autora'
```

Povedlo se?

{{ figure(
    img=static('merge.png'),
    alt="Výstup programu `gitk` s větvemi doplneni-autora a doplneni-nazvu sloučenými do master",
) }}

Pokud ano, můžeš staré větve vymazat – všechny jejich
změny jsou v `master` a nemá na nich cenu
pracovat dál.

```ansi
␛[36m$␛[0m git branch --delete doplneni-autora
Deleted branch doplneni-autora (was f1cd9be).
␛[36m$␛[0m git branch --delete doplneni-jmena
Deleted branch doplneni-jmena (was 5c9bf93).
␛[36m$␛[0m git branch
* ␛[32mmaster␛[m
```

Gratuluji, už umíš větvení a slučování!
