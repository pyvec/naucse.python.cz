# Linuxová administrace - mount

Vše na disku je uloženo jako sekvence bajtů. V rámci této sekvence jsou i údaje o souborech, složkách, atd. V unixu je vše soubor.

## Archivy

### Zip
- souborový systém v souboru
- na konci je adresář (obsah), kde je zapsáno kde je kolikátý soubor a jak je dlouhý
- nelze jednoduše zapisovat (nahradit jeden soubor větším)
- https://commons.wikimedia.org/wiki/File:ZIP-64_Internal_Layout.svg


## Souborový systém
- lze si představit jako objekt, který má určitou funkčnost (prohledávat addresáře, číst soubory, zapisovat informace, měnit vlsatnictví, atp.)
flash - fat32
windows - ntfs
linux - xfs, ext4

Soubory pro celý disk:
```
$ll /dev/disk
drwxr-xr-x. 2 root root 400 Nov  7 09:41 by-id
drwxr-xr-x. 2 root root  80 Nov  7 09:34 by-partuuid
drwxr-xr-x. 2 root root 120 Nov  7 09:34 by-path
drwxr-xr-x. 2 root root 160 Nov  7 09:41 by-uuid
```

### mount

- kde je připojený který souborový systém


```
$ mount
...
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime,seclabel)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
devtmpfs on /dev type devtmpfs (rw,nosuid,seclabel,size=8002676k,nr_inodes=2000669,mode=755)
...
```

- souborový systém `devtmpfs` je připojen na `/dev`
- tmp - pro dočasné soubory - filesystem tmpfs
```
lsblk
NAME                             MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
nvme0n1                          259:0    0 238.5G  0 disk  
├─nvme0n1p1                      259:1    0     1G  0 part  /boot
└─nvme0n1p2                      259:2    0 237.5G  0 part  
  ├─fedora_dhcp--0--123-root     253:0    0    50G  0 lvm   
  │ └─luks-e28e6e1b-f122-43d6-99d7-049dc034656f
  │                              253:2    0    50G  0 crypt /
  ├─fedora_dhcp--0--123-swap     253:1    0   7.7G  0 lvm   [SWAP]
  └─fedora_dhcp--0--123-home     253:3    0 179.8G  0 lvm   
    └─luks-0147c4fc-0301-4d1e-9cba-b0c17c700b48
                                 253:4    0 179.7G  0 crypt /home

```
TODO připojit flashku a doplnit lsblk


- disk může rozdělen na části, které mohou mít různé filesystemy
- abstrakce nad sebou
- jakým způsobem číst ze souboru je možné udělat různými způsoby
    - vzdálený přístup k serveru - síťová komunikace (pro nás soubor)

- mountpoint = přípojný bod
    - vše co je pod touto cestou je pod daným souborem

- /boot - zavaděč operačního systému
    - bios se podívá na začátek pevnýho disku a načte instrukce
- swap - pokud nestačí paměť - zapisuje se do toho prostoru
    - odkládají se méně používané věci z paměti


## gparted
- umí modifikovat struktury na disku !
- práva na spuštění má pouze superuživatel - může dojít k nesprávnému použití a zrušení systému

## ISO
- není možno modifikovat, pouze číst

```
$ls /mnt
```

- /mnt - k připojení různých zařízení jako flashky, disku, atp.
- můžeme sem připojit stažený soubor:
    - ```sudo mount /cesta/k/souboru /mnt```
    - obsah můžeme ověřit: `ls /mnt`
    - pokud máme cokoli v /mnt (před připojením), pak se k těmto souborům nyní nedostaneme, protože data směřují někam jinam - vhodné je např. vytvořit složku v /mnt a připojit zařízení tam

- odpojení připojeného prostoru:
    - `umount /mnt`



- knihovna libfuse/python-fuse na githubu
    - vytvořit si vlastní souborový systém - možný domácí úkol

- při náhlém odpojení počítače/souboru je možné, že se souborový systém poškodí
    - je možné se jej pokusit opravit pomocí `fsck` 

- raid - nejčastěji používaná technologie k duplikování dat


## Virtuální stroj
- můžu mít v počítači proces, který funguje jako celý další systém
- existuje několik programů, které jsou schopny virtualizovat počítač
    - Virtualbox, Boxes, atd.
    - vytvořit nový - můžeme vybrat ze souboru, začne se spouštět nová virtuálka
    - **poznámka pro příště: vybrat jedno ISO, které půjde nainstalovat všem (lite edice)** - vypadá to, že Alpine Linux Standard plní účel.







