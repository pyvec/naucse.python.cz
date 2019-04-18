{% set editor_name = 'VSCODE' %} {% set editor_url = 'https://code.visualstudio.com' %} 
{% extends lesson.slug + '/_base.md' %}

{% block name_gen %} Instalace VSCode{% endblock %}
{% block setup %}

Editor VSCode or Microsoftu podobně jako Atom funguje ihned po instalaci bez těžkého nastavování
Pokud ale chceš v editoru psát Python kód (nebo obecně každý jazyk) nainstaluj si rozšíření pro daný jazyk. 

## Instalace rozšíření pro Python

1. Otevři si VSCode editor.
2. V sloupci úpně na levo(šedý) klikni na ikonku rozšíření. Ve výchozí pozici
třetí od shora. Vypadá jako čtverec, který má v sobe ještě jeden.
3. Do vyhledávacího boxu zadej "Python".
4. Zvol první výsledek (v rohu je označen hvězdičkou).
5. V nově otevřeném okně klikni na modré tlačítko "Install".
6. Vyčkej, než se rozšíření nainstaluje. Editor se restartuje a zobrazí se ti okno nápovědy rozšíření.

## Spuštění kódu

Kód, který jsi vytvořil můžeš spustit přes zabudovaný terminál. Co to je a jak ho používat se dozvíš v dalších lekcích.

## Odesílání telemetrických dat

Tento textový editor odesílá data o tvém používání aby zlepšil uživatelské prostředí. Pokud si nepřeješ aby se nějaká data odesílala
navštiv prosím tento [link](https://code.visualstudio.com/docs/supporting/faq#_how-to-disable-telemetry-reporting).

## A to je vše!
Vše ostatní je již nainstalováno. Teď se jen pusť do samotného programování!

{% endblock %}
