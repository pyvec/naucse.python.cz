## Práce se soubory

Jak začneš psát trochu složitější programy,
mohlo by se stát, že tě konzole MicroPythonu začne trochu štvát.
Špatně se v ní opravují chyby a automatické odsazování funguje jen většinou.
Pojďme se podívat, jak naštvání předejít.

Nejdřív si do virtuálního prostředí nainstaluj program Ampy od Adafruitu.

```console
(env)$ python -m pip install adafruit-ampy
```

Doporučuji si větší kousky kódu – a určitě takové,
ve kterých je nějaký cyklus, podmínka či funkce –
psát v textovém editoru a do modulu pak posílat celý soubor.

Zkus si to. Do souboru `blikajici_led.py` dej následující kód:

```python
from machine import Pin
from time import sleep
pin_diody = Pin(14, Pin.OUT)
while True:
    pin_diody.value(0)
    sleep(1/2)
    pin_diody.value(1)
    sleep(1/2)
```

Potom zavři konzoli (`picocom`, PuTTY nebo `screen`).

Ke spuštění budeš potřebovat znát port:

* Linux: port používáš v příkazu `picocom`, např. `/dev/ttyUSB0`
* Windows: port používáš v PuTTY, např. `COM13`
* macOS: port používáš v příkazu `screen`, např. `/dev/tty.usbmodem*`

`ampy` spusť následujícím příkazem, jen za `PORT` doplň svůj port:

```console
(venv)$ ampy -p PORT run blikajici_led.py
```

Program by měl blikat diodou.
Využívá k tomu funkci `time.sleep()`, která počká daný počet vteřin –
tedy `time.sleep(1/2)` zastaví program na půl sekundy.

Podobně je možné na destičku soubory i nahrávat, jen je potřeba místo
`run` použít `put`.

```console
(venv)$ ampy -p PORT put blikajici_led.py
```

Pokud navíc budeš chtít, aby se program na destičce automaticky spouštěl, musí
se soubor s programem na destičce jmenovat `main.py`. `ampy` umí soubor při
kopírování i přejmenovat, když mu při kopírování zadáš i druhé (nové) jméno.

```console
(venv)$ ampy -p PORT put blikajici_led.py main.py
```

Po úspěšném kopírování máš na destičce nahraný náš program ze souboru
`blikajici_led.py` do souboru `main.py`. Teď už bude tvůj program fungovat
i bez počítače, takže stačí destičku připojit např. k powerbance
a dioda se rozbliká.
