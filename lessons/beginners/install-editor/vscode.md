{% set editor_name = 'Visual Studio Code' %} {% set editor_url = 'https://code.visualstudio.com' %} 
{% extends lesson.slug + '/_base.md' %}

{% block name_gen %}Instalace Visual studio code{% endblock %}
{% block setup %}

Editor Visual studio code (nebo zkráceně VS Code)od Microsoftu podobně jako Atom funguje ihned po instalaci bez těžkého nastavování.

## Stažení a instalace 

Editor jsi můžeš stáhnout na této [stránce] (https://www.code.visualstudio.com/.com). 
Na hlavní stránce vyber zelené tlačítko download a vyber instalátor pro svůj systém. 
Dále se jen řiď instrukcemi instalátoru jako u každého jiného programu. 

## Odesílání telemetrických dat

Tento textový editor odesílá data o tvém používání ([nejspíš včetně např.
obsahu otevřených souborů][privacy]).
Pokud si nepřeješ aby se data odesílala, můžeš odesílání zrušit:

* Otevři **File** > **Preferences** > **Settings** (macOS: **Code** > **Preferences** > **Settings**).
* Vyhledej `telemetry.enableTelemetry` a odškrtni tento záznam.

Viz též [původni postup v angličtině](https://code.visualstudio.com/docs/supporting/faq#_how-to-disable-telemetry-reporting).

[privacy]: https://privacy.microsoft.com/en-us/privacystatement


## A to je vše!
Vše ostatní je již nainstalováno/nastaveno. Teď se jen pusť do samotného programování!

{% endblock %}
