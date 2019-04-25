# Instalace editoru

Editor, program na úpravu textu, je základní pomůcka
každého programátora,
takže je dobré do něj investovat trochu času.

Je víceméně jedno, který programátorský editor budeš používat.
Pokud už nějaký oblíbený máš, stačí ho jen nastavit;
jestli ne, nějaký ti doporučíme.
Pokud ale používáš Poznámkový blok (Notepad) z Windows,
nebo TextEdit (editor předinstalovaný v macOS),
nebude ti stačit.
Stejně tak nejsou vhodné programy jako Word či Writer.


## Co programátorský editor umí

Editor pro programátory nám umožňuje upravovat *prostý text* – písmenka.
Na rozdíl od programů jako Word, Writer či Pages neumožňuje text *formátovat*,
tedy dělat nadpisy, obarvovat, zvětšovat font, vkládat obrázky a podobně.

Pomocí editoru budeme zadávat počítači příkazy, takže formátování nepotřebujeme.
Porovnej {{ gnd('sám', 'sama') }}, jaký je rozdíl mezi následujícími příkazy
pro někoho, kdo se jimi má řídit:

* Nakresli mi beránka!
* <font color="green">Nakresli <big><big>mi</big> <u>beránka</u>!</big></font>

To, že neumí formátování, neznamená že jsou naše editory úplně „hloupé“
nástroje.
Aby se nám programy upravovaly pohodlněji, mají několik vychytávek:

Podpora více souborů
:   Větší projekty sestávají z více souborů, které můžeš mít v editoru
    otevřené všechny najednou.

Číslování řádků
:   Před každým řádkem se ukazuje číslo.
    To se bude velice hodit, až Python bude nadávat, že chyba je na řádku 183. 

Odsazování
:   V Pythonu je důležité, kolika mezerami řádek začíná.
    Správně nastavený editor nám odsazování značně zjednoduší.

Obarvování
:   Ačkoli nemůžeme u jednotlivých písmenek nastavovat barvu přímo, editor nám
    obarvením může napovědět, jak našim instrukcím bude počítač rozumět.
    Ale je to jenom nápověda:
    programátor s jinak nastaveným editorem může mít stejný soubor obarvený
    docela jinak.

> [note]
>
> Pro ilustraci, takhle může v editoru vypadat kousek kódu:
>
> ```python
>     1  @app.route('/courses/<course:course>/')
>     2  def course_page(course):
>     3      try:
>     4          return render_template(
>     5              'course.html',
>     6              course=course,
>     7              plan=course.sessions,
>     8          )
>     9      except TemplateNotFound:
>    10          abort(404)
> ```


## Volba a nastavení editoru

Vybereš-li editor, klikni na jeho jméno a dostaneš se na instrukce ke stažení
a nastavení.
(Na tuhle stránku se pak už nemusíš vracet.)

* [Visual Studio Code]({{ subpage_url('vscode') }}) – doporučený editor pro
  Windows a macOS (a vhodný i pro Linux).
  V poslední době je to asi nejpopulárnější editor kódu.
  Nabízí mnoho funkcí a má velkou základnu uživatelů a vývojářů,
  takže se neustále vylepšuje.

Na Linuxu budeš mít pravděpodobně už nainstalovaný Gedit nebo Kate.
Zkus se podívat do systémové nabídky, jestli jeden z nich máš (případně je
spusť z příkazové řádky jako `gedit`, resp. `kate`).
Pokud ano, klikni na odkaz níže a editor si nastav.
Nemáš-li ani jeden, vyber Visual Studio Code (viz výše).

* [Gedit]({{ subpage_url('gedit') }}) – bývá na systémech s prostředím GNOME.
* [Kate]({{ subpage_url('kate') }}) – bývá na systémech s prostředím KDE.

Existují i jiné editory, na které máme návody
nebo jsme je doporučovali ve starších verzích těchto materiálů.
Pokud se jeden z nich rozhodneš použít, neuděláš chybu:

* [Atom]({{ subpage_url('atom') }}) – kvalitní editor s jednoduchým designem
* [Notepad++]({{ subpage_url('notepad-plus-plus') }}) – nenáročný editor
  pro Windows vhodný pro pomalejší počítače

Máš-li už svůj oblíbený editor – Vim, Emacs, Geany, apod., použij ten:

* [Ostatní]({{ subpage_url('others') }}) – máš-li jiný editor, zkontroluj
  si že je správně nastaven.


### IDE

Existují i složitější a mocnější editory, takzvané *IDE* (angl. *Integrated
Development Environment*, integrované vývojové prostředí),
třeba [PyCharm], [Eclipse] nebo [KDevelop].
Umí spoustu pokročilých funkcí, které programátorům pomáhají:
našeptávání, přejmenovávání, spouštění programů, správu virtuálních prostředí
a podobně.
Na začátek ale nejsou moc vhodné.

Chceš-li takový editor přesto použít, měl{{a}} bys ho už poměrně dobře znát:
vědět, co za tebe dělá editor a jak to spravit, až něco udělá špatně.
{% if var('coach-present') -%}
Koučové většinou znají jen jeden editor – ten, který používají –
takže nemusí být schopní s pokročilým IDE rychle pomoct.
{%- endif %}

[PyCharm]: https://www.jetbrains.com/pycharm/
[Eclipse]: https://eclipse.org/
[KDevelop]: https://www.kdevelop.org/

