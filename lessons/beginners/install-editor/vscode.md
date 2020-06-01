{% set editor_name = 'Visual Studio Code' %} {% set editor_url = 'https://code.visualstudio.com' %} 
{% extends lesson.slug + '/_base.md' %}

{% block name_gen %}Visual Studio Code{% endblock %}

{% block install %}
## Stažení a instalace 

Editor si můžeš stáhnout z jeho [domovské stránky](https://code.visualstudio.com/).
Vyber na ní zelené tlačítko Download a vyber instalátor pro svůj systém.
Dále se řiď instrukcemi instalátoru jako u každého jiného programu.
{% endblock %}

{% block setup %}
Ve Visual Studio Code se nemusí nic nastavovat, funguje „od výroby“ tak, jak má.

### Odesílání telemetrických dat

Tento textový editor ale odesílá data o tvém používání ([nejspíš včetně např.
obsahu otevřených souborů][privacy]).
Pokud si nepřeješ aby se data odesílala, můžeš odesílání zrušit:

* Otevři **File** > **Preferences** > **Settings** (macOS: **Code** > **Preferences** > **Settings**).
* Vyhledej `telemetry.enableTelemetry` a odškrtni tento záznam.

Viz též [původni postup v angličtině](https://code.visualstudio.com/docs/supporting/faq#_how-to-disable-telemetry-reporting).

[privacy]: https://privacy.microsoft.com/en-us/privacystatement


{% endblock %}
