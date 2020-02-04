# Linuxová administrace 5.12.2019

> Dneska si vyzkoušíme přehrávat zvuky
> 

1. zkus si přehrát nějaký zvuk
2. zkus si to z příkazové řádky
3. jaké zvuky máš na počítači?

## Příkaz `locate`

Tento příkaz vypíše seznam všech souborů, které mají v názvu
```
$ locate .mp3
```

Ten funguje tak, že je to daemon, který jednou za čas projde celý disk a zaindexuje všechny soubory.

Pokud sis tento příkaz právě nainstalovala, tak ti ještě nic neřekne, protože je jeho databáze zatím prázdná. Tu si můžeš nechat vytvořit/zaindexovat pomocí `updatedb` (nutno spouštět jako `root`, či se `sudo`).

## Přehráváme zvuky z příkazové řádky
> Proč se hodí to mít v příkazové řádce?

Protože to můžeme **automatizovat**. Třeba spouštět stále dokola.

```
$ while ; do mplayer <cesta/k/tvemu/zvuku>; done
```

(až to budeš chtít zrušit, zmáčni `Ctrl+C`).

My si to zkusíme s přehrávačem `mplayer`.

Pokud jsi na Fedoře a nejde ti zvuk přehrát, protože chybí kodeky, nainstaluj si repozitář `free` z  https://rpmfusion.org/Configuration

## Spouštění zvuku podle času

Dneska si vyzkoušíme, jak spustit zvuk v zadaný čas.

O spouštění programů podle času se stará démon `cron`.

```
$ man cron
```

Tady se ale nedočteme, jak vypadá konfigurace.

`man` má více *kapitol*. Tím se dostaneme do kapitolo `1`, kde je napsané, jak se zadaný příkaz spouští a jaké má parametry.

```
$ man 5 cron
```
TODO: ověřit příkaz výše

```
$ crontab -e
```

Otevře se nám editor, do kterého napíšeme:

```
* * * * * mplayer /desta/k/zvuku
```
Každá z hvězdiček vyjadřuje jinou část času (hodina, minuta, ...). Abychom si to ale nemuseli pokaždé číst znova, doporučuji si na první řádek dá komentář, co která pozice říká.

```
# min hod den mesic den_v_tydnu prikaz
```

Když to uložíte a zavřete, tak by se měl nainstalovat.

A teďka vám to každou minutu přehraje zvuk. Jupí! :relaxed:

Toto nastavení vydrží i po vypnutí počítače. Zkrátka dokud si to zas nevypneš.

Teďka si vyzkoušíme, jak hlídat třeba volné místo na disku.

`df`

TODO: doplnit výpis

což vypíše 

```
df -h
```

to vypíše hezky v kB, MB, GB...

Jenže nám to vypíše aktuální stav a pak se ukončí.

## Příkaz `watch`

Příkaz `watch` nám spouští zadaný příkaz každé 2s.

```
$ watch df -h
```

```
$ watch date
```


```
$ watch -d 
```
Todo zvýrazní rozdílné znaky od minulého zobrazení.


Pokud bychom to chtěli spouštět častěji, tak to zařídíme pomocí `-n` (čas v sekundách), takže třeba:
```
$ watch -n0.2 date
```

Ukončíš to přes `Ctrl+C`.

```
$ date -Is

$ date -Id

$ date -Im
```
TODO: doplnit výstupy

To je dostatečně hezký formát, aby se to dalo použít jako název souboru. Na linuxu nějaké dvojtečky a pluska v názvu souboru nevadí, ale na Windows by to zlobilo.

Teďka si zkusíme snížit frekvenci, jak často se nám to bude přehrávat. Třeba každou 50. minutu.

```
$ crontab -e
50 * * * * mplayer /cesta/ke/zvuku
```

`*` znamená každou/každý

Každý druhý den se napíše:
```
$ crontab -e
0 0 /2 * * mplayer /cesta/ke/zvuku
```

Znamená 2. den v měsíci
```
$ crontab -e
0 0 2 * * mplayer /cesta/ke/zvuku
```

[nakopírovat kus z EXAMPLES]

Cron může posílat emaily. Email je věc starší, než je internet. Původně se emaily posílaly v rámci jednoho počítače

Příkazem `mail` si je můžeme zobrazit. Po čase je dobré se podívat, jestli je nám `cron` neposílá, což by nám po čase mohlo 


Proč jsme si zkoušeli `cron` na zvucích? Protože když se v zadaný čas spustí, tak nemá k dispozici příkazovou řádku. Takže 

# Ansible

Příklad: Mám k dispozici spoustu počítačů, kde provádím zálohy

* chci změnit intrval zálohy
* napíšu si cyklus, který se přes SSH připojí k tomu počítači
* změním v `crontab`u ten interval

Jenže pak zjistím, že u 54. se to jaksi nepovedlo.


* tak si někam napíšu, co se tam má provést

* když mi shočí jeden z těch serverů, tak to spoustím znova
* verzování v gitu
* píše se to ve formátu `yml`

## Příklad: nainstalujeme si nějaký *užitečný program*
```
# setup.yml

- hosts: localhost
  connection: local
```

Pokud bychom to používali i s dalšími počítači, tak ty se definují v samostatném souboru.

Abychom mohli něco nainstalovat, je třeba býti `root`em.
```
   become_user: root
```

Dál se píší - ne příkazy - ale popis, jak chcete, aby ten cílový systém vypadal.

```
   tasks:
   - name: Install htop
     become: yes
```

Teďka podle toho, jaký linux používáš se bude tato část lišit. Pro Fedoru:
```
     dnf:
        state: latest
        name:
        - htop
```

Pro Debian, Ubuntu by tento blok vypadat:
```
     apt:
        state: latest
        name:
        - htop
```

Celý blok nakonec vypadá takto:
```
- hosts: localhost
  connection: local
  become_user: root
  tasks:
   - name: Install htop
     become: yes
     dnf:
        state: latest
        name:
        - htop
```

Tím `state: latest` říkáme, že chceme nainstalovat nejnovější dostupnou verzi.

A teďka to zkusíme spustit:

```
$ ansible-playbook -K setup.yml
```

Díky parametru `-K` se nás Ansible nejdřív zeptá na sudo heslo a s tím pak spoustí celý playbook.

Pokud máte nainstalovaný `cowsay`, můžeme si to zkusit odinstalovat. Celý blok výše si zkopírujeme a upravíme následovně:

```
- hosts: localhost
  connection: local
  become_user: root
  tasks:
   - name: Uninstall cowsay
     become: yes
     dnf:
        state: absent  # present pro instalaci
        name:
        - cowsay
```

TODO: doplnit výpis, kde je vidět "changed" při deinstalaci balíčku.

Když ten playbook spoustíme znova, tak to sice chvilku trvá, ale už nám to řekne "ok=3", protože to už nic nezměnilo.

Tento příklad se připojuje pouze k aktuálnímu počítači. Pokud bychom to chtěli pouštět i na jiných počítačích, je třeba je zapsat do takzvaného *inventáře* (inventory file).

### Perlička na závěr

Když napíšu `ls`, tak to často vypíše barevný výstup. Jak to dělá? A hlavně, jak si to udělám já?

Střípek z historie:
> terminál, tiskárna, nebyl backspace ani Esc, protože ten překlep už byl vytisknutý na papíře. U grafických terminálů to už šlo. A tak se řešilo, jak to udělat. ASCII znak ESC.

Takový ascii znak na klávesnici nenajdeme, proto si to napíšeme v pythonu.

```python
# barvicky.py
print('\x1B[1;31m slovo')
```

TODO: ukázka obarveného i promptu
```
       +--- tzv. escape sekvence
       |
    ------
\x1B[1;31m
----
  |
  +--- je jediný znak, a to ASCII ESC
```

Kdy to přestane psát červeně? Až zavřeme terminál, nebo až napíšeme reset sekvenci.


```python
print('\x1B[1;31m slovo   \x1B[0m')
```


```python
for i in range(30, 40):
    print(f'\x1B[1;{i}m slovo   \x1B[0m')
    
for i in range(40, 50):
    print(f'\x1B[1;{i}m slovo   \x1B[0m')
    
# doplnit kus kodu
```

S těmito sekvencemi je problém, protože různí dodavatelé terminálu si je implementovali po svém. To se sice standardizovalo do ANSI, ale stejně je dobré na to použít nějakou knihovnu, třeba `click` v pythonu.

```python
for i in range(100):
    print(i, end='\r')
    time.sleep(1)
```

Takto se například dají vykreslovat progressbary. Má to ale i svá úskalí, například změna velikosti terminálu a tak. Určitě si na to nainstalujte knihovnu, která to správně vyřeší za vás.

Na Windows to fungovat nebude, tam se to řeší přes systémové volání. 

Terminálé editory fungují právě na tomto principu escape sekvencí.
```
$ vi > /tmp/session
```

Můžete si je zobrazit třeba přes:
```
less /tmp/session
```
