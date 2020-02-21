# Domácí projekty

Naprogramuj jednoduchou webovou aplikaci pomocí frameworku Flask.

# Webová aplikace ve Flasku

Aplikace bude mít dva endpointy. První bude home page s uvítáním a návodem, co může uživatel na stránkách najít.
Druhý bude poskytovat informace podle zadaného klíče.

## Data v aplikace

U sebe na počítači si vytvoř textový soubor s příponou `.txt`, kde bude JSON s daty ve formě klíč: hodnota.
Můžeš si vymyslet jaká data chceš. Telefonní seznam - jméno: telefonní číslo, knihu básní - autor: báseň nebo třeba seznam vánočních dárků, které chceš koupit - obdarovaný: dárek.
Můžeš se inspirovat v lekci o JSONu.

```python
json_string = """
    {
      "name": "Anna",
      "city": "Brno",
      "language": ["czech", "english", "Python"],
      "age": 26
    }
"""
```

## Poskytování dat

Endpoint, který bude poskytovat data musí mít dynamickou URL. Jak vytvořit takový endpoint najdeš v lekci FLask v sekci `Dynamické routy`.
Místo `<username>` bude tvůj endpoint přijímat argument např. jméno, autor básně, obdarovaný.
Uvnitř něj si otevřeš a načteš soubor s JSONem. Soubor nezapomeň otevírat pomocí `with open(...`. Obsah souboru si nahraješ do pythonního slovníku pomocí `json.loads`. Jak na to najdeš v lekci o JSONu v sekci `JSON v Pythonu`. Podle zadaného klíče vybereš potřebné hodnoty ze slovníku a vrátíš je.

Po nahrání JSONu se tvoje data budou chovat jako klasický pythonní slovník a jak vybírat ze slovníku podle klíče už známe. 

Nezapomeň ošetřit situaci, kdy uživatel zadá klíč, který nebude ve slovníku. To můžeš vyřešit nějakou hezkou hláškou. Pokud si troufneš, můžeš uživateli pomocí Flaskové funkce `abort` vrátit stavový kód 404 - nenalezeno. Dokumentaci k `abort` můžeš najít tady: https://flask.palletsprojects.com/en/1.1.x/api/#flask.abort


### Odevzdání

Řešení nezapomeň nahrát na github společně s JSONem s daty.


# Bonusy

Pojem, který by měly znát všechny vývojářky webových aplikací je [MVC pattern](https://www.tutorialspoint.com/mvc_framework/mvc_framework_introduction.htm). Co to znamená jsme lehle naťukli na lekci, kdy jste podle tohoto patternu psali svojí Flask aplikaci. Tady jsme mluvili o tom, že další webový framework Django používá MVT pattern a že jsou vlastně velmi podobné. Rozdíl mezi MVC a MVT najdete [zde](https://medium.com/shecodeafrica/understanding-the-mvc-pattern-in-django-edda05b9f43f).