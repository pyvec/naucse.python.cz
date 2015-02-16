import requests

resp = requests.get('http://python.cz')

print(resp.text)


# https://dev.twitter.com/rest/public

import base64
import pprint
from urllib.parse import quote

import requests

# z https://apps.twitter.com/
# (access_token je nejdřív None; doplnit po prvním přihlášení)
from kody import api_key, api_secret, access_token


def get_access_token():
    # viz https://dev.twitter.com/docs/auth/application-only-auth
    secret = quote(api_key) + ':' + quote(api_secret)
    secret_b = secret.encode('ascii')
    secret_64 = base64.b64encode(secret_b)
    secret_s = secret_64.decode('ascii')

    headers = {
        'Authorization': 'Basic ' + secret_s,
        'Host': 'api.twitter.com',
    }
    response = requests.post('https://api.twitter.com/oauth2/token',
                            headers=headers,
                            data={'grant_type': u'client_credentials'})

    print('Dotaz:')
    print(response.request.headers)
    print(response.request.body)

    print('Odpověď:')
    print(response.headers)
    print(response.text)

    pprint.pprint(response.json())
    return response.json()['access_token']

if not access_token:
    access_token = get_access_token()
    print('Token: ', access_token)

def bearer_auth(request):
    request.headers['Authorization'] = 'Bearer ' + access_token
    return request

session = requests.Session()
session.auth = bearer_auth

response = session.get(
    'https://api.twitter.com/1.1/search/tweets.json',
    params={'q': '#vesmír'},
)
response.raise_for_status()
data = response.json()

pprint.pprint(dict(response.headers))

for tweet in data['statuses']:
    print(tweet['id_str'])
    print(tweet['text'])

