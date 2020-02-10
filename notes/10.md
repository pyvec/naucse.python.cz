# Syscalls, kontejnery

# "šipečky"
## `>>`

`$ echo "Ahoj" > pozdrav`
```
$ cat pozdrav
Ahoj
```
`$ echo "Zdravim" >> pozdrav`
```
$ cat pozdrav
Ahoj
Zdravim
```

## heredoc
Slouží k zapsání (zpravidla) z víceřádkového textu jako hodnoty.

```
$ cat << END
...
ABCD
efgh
END
```

```
$ cat <<< "Abcdef"
Abcdef
```


# místo na disku
`$ df` - zobrazení obsazenosti disku, přepínač 'h' pro zobrazení pro lidi


# syscalls

**jádro**
* přepíná mezi běžícími procesy, aby to vypadalo, že běží všechny najednou.
* zprostředkovává např. otevírání souborů soubory
* "chci přečíst např. 20 bajtů ze souboru 3 (`3` je file descriptior)"

```
+--------+    +--------+
|        |    |        |
| proces |    | proces |
|        |    |        |
+---+----+    +----+---+
    ^              ^                +------------------+
    |              |                |                  |
    |              |                | Soubory na disku |
    v              v                |                  |
+---+--------------+---+            +------------------+
|                      |                   |
|        jádro         |-------------------+
|                      |
+----------------------+

```

Nakresleno pomocí: http://asciiflow.com/

## sledování syscalls `strace`
```
$ strace echo
execve("/usr/bin/echo", ["echo"], 0x7ffed87ac530 /* 59 vars */) = 0
brk(NULL)                               = 0x564fe1290000
arch_prctl(0x3001 /* ARCH_??? */, 0x7ffd4c975070) = -1 EINVAL (Invalid argument)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=109457, ...}) = 0
mmap(NULL, 109457, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7fdbbd5a9000
close(3)     
...
+++ exited with 0 +++
```
strace - vypíše všechny volání, které program používá
volání `open` - návratová hodnota je file descriptor
`read(3, [...])`, `[...]` je obsah paměti, kam se zapíše přečtený obsah
nakonec se zavolá `close(1)`, kde `1` je standartní výstup
nakonec se zavolá `close(2)` a `2` je chybový výstup


`strace python`
... ve výstupu je vidět `read` jak čtou po jednotlivých znacích

K čemu to může být dobré? Občas se hodí vědět, které soubory program otevírá.


# Kontejnery
Když já jako vývojář něco napíšu, tak mi to funguje... jenže pak to pošlu kolegovi a tomu to neběží, protože v `/etc/neco` jsem něco zapoměl poslat. To systémovým administrátorům vadí a kontejenry to řeší.

* izolace
    * spuštění programů, kterým *nevěřím*
* na všech systémech to je stejné

Může existovat zvláštní proces, který pod `/etc/kdesi/cosi` vidí úplně jiné soubory, než ostatní. Tak samo aji s uživateli, které ten proces vidí.

Každý kontejner má svůj vlastní filesystem, který je třeba mu *nakopírovat*.

- rozdíl virtuální počítač vs kontejner
    - virt. počítač - má vlastní systém, vlastní procesy
    - kontejner - proces v počítači, je to zvláštní program (něco jako virtuální prostředí)

### `overlayfs`
* první vrstva - základní souborový systém
* druhá vrstva - zde se ukládají změny (rozdíl oproti základnímu systému)

 > Paralela se změnami v zákonech

K čemu to je dobré? Kontejnery mohou mít stejný základ, ale pak se už liší jen v té hornější vrstvě. Např. mám 2 webové aplikace. Jedna napsaná v knihovně Flask a druhá v Djangu. Obě tak mohou používat stejný základ

TODO: doplnit obrázek z tabule.

Docker je jedna z implementací kontejnerů.

https://hub.docker.com/_/postgres

instalace do systému na Fedoře vs. Ubuntu - nastavení se budou lišit -> potencionální zdroj problémů.
zato když to spustíš z kontejneru, tak tam je ten operační systém vždy stejný.

Má to blízko k *virtuálnímu počítači*. Hlavní rozdíl je v tom, že virtuální počítač používá proces, co se navenek tváří jako procesor

## Instalujeme `docker`

* nainstalujeme balíček `docker`

* `sudo systemctl start docker`
    * (?) jaký je rozdíl mezi `start` a `enable`
    * `enable` zajistí, aby se ten démon spouštěl při startu počítače

Když budete spouštět příkazy `docker ...`, bude po vás pravděpodobně chtít to spustit jako uživatel `root`. Ten pak komunikuje s `docker` démonem.

Raději se ale přidejte do skupiny `docker`.
```
$ sudo usermod -a -G docker $(whoami)
```

Případně `docker` vyměň za `podman`
```
$ docker pull httpd
(... stahování vrstev ...)
```


### `podman`
Jedná se o implementacit ypickou pro Fedoru.
Ve Fedoře 31 je docker rozbitý a zkus si to v `podman`.
Narozdíl od `docker` nepotřebuje práva roota a pro naši potřebu to bude fungovat stejně.
``` 
`$ sudo dnf install podman`
$ podman pull httpd
```

Stáhlo to spoustu blobů. To jsou jednotlivé vrstvy. Pokud už nějakou máš nainstalovanou z dřívějška, rovnou se použije.

`$ podman run -it ubuntu` - stáhne a spustí příkazovou řádku z kontejneru Ubuntu.

Tam si zkus spustit:
```
$ cat
```

Pak si v jiném terminálu (hostitelského systému) spusť `htop` a pomocí F5 si zobraz stromový výpis. Ve výpisu najdeš běžící proces `cat` z toho kontejneru.

Pokud bych to samé udělal ve virtuálním počítači, tak tam najdeš jen proces, který dělá virtuální procesor, ale už ne procesy, které se na něm spouští.

Proto je možné např. ukončit proces v kontejneru z hlavního systému. Jen vidí jiný souborový systém a jsou omezeny.

Pro vyskočení z ubuntí příkazové řádky stačí ukončit terminál, například příkazem `exit`.


`$ podman images`
- vypíše seznam všech stažených kontejnerů

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
httpd               latest              2ae34abc2ed0        13 days ago         165MB
ubuntu              latest              775349758637        5 weeks ago         64.2MB
```

- vypíše seznam všech právě běžících kontejnerů
```
$ podman ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
c9f835211bbb        ubuntu              "/bin/bash"         39 seconds ago      Up 38 seconds                                   focused_khayyam
```

```
$ podman ps --all

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
4a523c41344d        ubuntu              "/bin/bash"         10 minutes ago      Exited (0) 2 minutes ago                        nostalgic_williams
697cccb2c307        ubuntu              "/bin/bash"         12 minutes ago      Exited (0) 11 minutes ago                       jovial_keller
```

Images můžeme klidně smazat pomocí `$ podman rm <container-id>`

Jaký je rozdíl mezi kontejnerem a image?
*image* je obraz disku, nedá se změnit.

*kontejner* je něco jako proces, je instance image

Image mohu smazat jedině pokud neběží žádný kontejner, který z něj běží.

Image může být založen i na jiném image.


```
$ podman run -ir httpd
```

nespustí příkazovou řádku, ale spustí přímo ten server httpd na popředí. Žádní démoni ani jiní pokémoni.

I přesto můžu můžu 
```
$ podman run -ir httpd bash
```

`-it` říká, že chci kontejner spustit interaktivně a na popředí, což se nám hodí pro `bash`.


```
podman run -p 8080:80 httpd
```
Port `8080` je port na straně kontejneru, která se zpřístupní na portu `80` na tvém (hostitelském) počítači.

Zkusíme si zpřístupnit nějaký vlastní adresář dovnitř kontejneru.

Nejdříve si vytvoř soubor `index.html`
```
$ echo Ahoj! > index.html
```

A teďka si zkusíme 
```
$ podman run -p 8080:80 -v "$PWD":/usr/local/apache2/htdocs/:Z httpd
```

Někdy je potřeba použít i `:Z`, což nám zpřístupní soubory z domovského adresáře (standartně to totiž je zakázané).

## Dockerfile

Vytvoř si soubor `Dockerfile` (musí být psané s velkými písmeny)
```
FROM httpd
RUN echo Ahoj > /usr/local/apache2/htdocs/index.html
```

```
$ podman build -t mujhttpd .
```

```
$ podman run -p 8080:80 -v mujhttpd
```

Takový hotový kontejner se dá pak pushnout do dockerhubu.

Jde to dokonce spustit aji na Windows! (Tam se vytvoří virtuální stroj s linuxem a v něm se to pak spustí).
