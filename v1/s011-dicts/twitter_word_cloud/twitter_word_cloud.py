import string
import jinja2
import json
import twitter_timeline
import oauth_info


def odstran_interpunkci(retezec):
    znaky_interpunkce = string.punctuation.replace('#', '').replace('@', '')
    for znak in znaky_interpunkce:
        retezec = retezec.replace(znak, '')
    return retezec


def najdi_klicova_slova(text):
    klicova_slova = []
    for slovo in text.split():
        if slovo.startswith('#') or slovo.startswith('@'):
            klicova_slova.append(slovo.lower())
    return klicova_slova


def spocitej_frekvence(slova):
    # Napocitej vyskyt kazdeho slova
    frekvence_slov = {}
    for slovo in slova:
        if slovo in frekvence_slov.keys():
            frekvence_slov[slovo] += 1
        else:
            frekvence_slov[slovo] = 1

    # Spocitej relativni frekvenci
    for slovo, frekvence in frekvence_slov.items():
        frekvence_slov[slovo] /= len(slova)

    return frekvence_slov


def slovnik_jako_seznam_tuplu(slovnik):
    seznam = []
    for slovo, hodnota in slovnik.items():
        seznam.append((slovo, hodnota))
    return seznam


def odstran_malo_casta(frekvence_slov):
    caste = {}
    for slovo, frekvence in frekvence_slov.items():
        if frekvence > max(frekvence_slov.values()) / 20:
            caste[slovo] = frekvence
    return caste

# ZISKANI DAT
timeline = twitter_timeline.TimelineMiner(
    oauth_info.ACCESS_TOKEN,
    oauth_info.ACCESS_TOKEN_SECRET,
    oauth_info.CONSUMER_KEY,
    oauth_info.CONSUMER_SECRET,
    oauth_info.USER_NAME
)
if timeline.authenticate():
    print('Prihlaseni do Twitteru probehlo uspesne.')

timeline.get_timeline(max=2000)

# NORMALIZACE DAT A SPOCITANI FREKVENCE SLOV
text = ' '.join(timeline.tweets)

text = odstran_interpunkci(text)

slova = najdi_klicova_slova(text)

frekvence_slov = spocitej_frekvence(slova)

frekvence_slov = odstran_malo_casta(frekvence_slov)

# VYKRESLENI MRAKU
loader = jinja2.FileSystemLoader(searchpath='./')  # Kde ma Jinja2 hledat sablony?
env = jinja2.environment.Environment(loader=loader)  # Inicializuj Jinja2 prostredi
frekvence_json = json.dumps(frekvence_slov)  # Preved slovnik do formatu, kteremu rozumi JavaScript
template = env.get_template('wordcloud.jinja2')  # Nacti pripravenou sablonu

# Priprav data pro sablonu
template_data = {
    'words': frekvence_json,
    'width': 1200,  # Sirka mraku
    'height': 1200,  # Vyska mraku
    'rescale': 1500  # Jake rozpeti velikosti ma byt mezi slovy?
}

# Vykresli HTML stranku a uloz do souboru
with open('wordcloud.html', 'w') as result_file:
    result_file.write(template.render(template_data))
