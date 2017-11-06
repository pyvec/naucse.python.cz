Deployment webových aplikací
============================

Aplikace napsaná v Pythonu běží na našem počítači, ale jak ji dostat do Internetu?
Existují různé možnosti, jednou z nich je nasadit ji do cloudu.

> [note]
> Nemáte ještě webovou aplikaci? Můžete vyzkoušet framework
> [Flask](../../intro/flask/).

### WSGI

Nasazování webových aplikací v Pythnu se opírá o WSGI,
což je standardní pythonní rozhraní pro komunikaci
mezi webovou aplikací a webovým serverem definované v [PEPu 333][PEP333].

Naprostá většina webových frameworků v Pythonu toto rozhraní implementuje přímo,
případně k tomuto účelu obsahuje wrapper.

Je tedy jedno, jestli používáte Flask, Pyramid, Django, Bottle nebo Falcon,
vždy vaší aplikaci představuje `application` objekt, který se navenek chová
stejně. Webové frameworky implementují aplikační část WSGI.

Stejně tak existují webové servery, které implementují serverovou část WSGI,
například [Gunicorn] nebo `mod_wsgi` pro `httpd` (Apache). Tyto servery umí
pracovat s `application` objektem a nezajímá je, v jakém frameworku je aplikace
napsaná.

[PEP333]: https://www.python.org/dev/peps/pep-0333/
[Gunicorn]: http://gunicorn.org/

Většině cloudových providerům stačí nějakým způsobem `application` objekt předat
a o zbytek se postarají za vás. Jedním z takových providerů je i
[PythonAnywhere](https://www.pythonanywhere.com/).

Deployment webových aplikací na PythonAnywhere je popsaný v lekci
[PythonAnywhere]({{ subpage_url('pythonanywhere') }}).
