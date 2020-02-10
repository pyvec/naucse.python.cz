Linuxová administrace

## Co je potřeba

- 1 virtuálka
- nepotřebuje připojení na Internet
- potřebuje síťování s opravdovým počítačem (může být i Windows/Mac)
- ditribuce se systemd

Fedora Server network install: https://alt.fedoraproject.org/

### Síťování 
- Virtualbox:
    - Síť pouze s hostem


## Instalace balíčků
- pomocí balíčkovacích systémů (rpm, deb)
- samotný balíček obsahuje:
    - soubory
    - metadata 
    - závislosti

- nádstavba nad rpm je dnf, který např. pomáhá s vyhledáním závislostí
    
    ```
    $ rpm -q bash
     bash-5.0.7-1.fc30.x86_64
     ```
     `rpm -q -l bash` - zobrazí soubory balíčku
    `rpm -q --requires bash` - jaké balíčky potřebuje bash, aby mohl být nainstalován
    `sudo dnf install [package]` - instalace balíku
    `sudo dnf update` - aktualizace všech balíčků i nainstalování nových závislostí
    `systemctl` - velký seznam, co běží na serveru (procesy, připojené souborové systémy, logování, nastavení automatického času, internetové připojení, atd.)
    
## Repozitář 
- místo na internetu, které obsahuje množství balíčků
- pro fedoru je vhodné povolit repozitář rpmfusion (hlavně pro videa)
    - free - svobodný kód
    - nonfree - skype, stream, atp.
- repozitáře ve fedoře se nacházejí v `/etc/yum.repos.d/`


## Firewall
- síťové zařízení, které povoluje/blokuje připojení podle zadaných parametrů
- každá služba má přiřazený port, na kterém pracuje
    - webserver má port 80(http), 443(https)

- fedora - povolení webserveru:
    `$ firewall-cmd --add-service=http` -> nyní dovol spojení na portu pro http
    `success`
    `$ firewall-cmd --permanent --add-service=http` -> zapíše, že má být povolen port pro http po dalším startu


## Webový server
- instalace `dnf install httpd`, potvrdit pomocí `y`
    ```
    $ rpm -q -l httpd
    /etc/httpd/conf
    /etc/httpd/conf.d/autoindex.conf
    /etc/httpd/conf.d/userdir.conf
    /etc/httpd/conf.d/welcome.conf
    /etc/httpd/conf.modules.d
    /etc/httpd/conf.modules.d/00-base.conf
    /etc/httpd/conf.modules.d/00-dav.conf
    ...
    ```

    `systemctl start httpd` -> spustí se služba httpd - příslušný proces
    `systemctl status httpd` -> zobrazí stav služby (jestli běží, na jakém portu poslouchá, seznam procesů, atp.)
    `systemctl stop httpd` -> vypne se httpd
    
- po zadání z hostujícího počítače `curl IP_adresa_virtualniho_pocitace` lze získat webovou stránku
- lze nainstalovat verzi textového prohlížeče do virtuálního počítače, např. links: `dnf install links`, spustí se pak příkazem `links google.com`
    - `$ links IP_adresa_virtualniho_pocitace` zobrazí stránku našeho webserveru
    - pomocí 'q' opustíme links
- pro spuštění webserveru po startu systému
    - `systemctl enable httpd`
    - `systemctl restart httpd` a `systemctl reload httpd`
        - restart služby httpd, rozdíl mezi restart a reload je, že v případě reload se pouze načtou změny v konfiguračních souborech a připojení k webserveru zůstanou aktivní. V případě restartu se ukončí vše.
- nastavení v: `/etc/httpd/conf.d/`
    - můžeme provést změnu v `/etc/httpd/conf.d/welcome.conf`, například vše zakomentovat. Tento soubor definuje, pokud se někdo podívá na domovskou stránku, tak se zobrazí určitý obsah. Po našem zakomentování se bude zobrazovat něco jiného.
        - je nutné použít `systemctl reload httpd` (příp. restart) pro zobrazení změn
- DocumentRoot
    - adresář, který disponuje soubory pro webový server
    - typicky `/var/www/html/`
    - vytvořme si soubor `hello.txt` v tomto adresáři s libovolným obsahem
        - ověřme si, že si tento soubor lze zobrazit v prohlížeci
- UserDir
    - pokud má uživatel adresář `public_html`, pak tento adresář lze zobrazit pod /~user/
    - defaultně vypnuté, protože se může jednat o bezpečnostní riziko


## DÚ
- vytvořit si nového uživatele
- Povolit uživatelské webové stránky
- Zveřejnit nějaký obsah pomocí webového serveru

Dokumnetace je v komentářích v `/etc/httpd/userdir.conf`


