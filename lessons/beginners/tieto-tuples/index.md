## N-tice (Tuples)

N-tice jsou neměnnou variantou seznamů. Proč jej potřebujeme? Mimo jiné slouží jako klíče k slovníkům, viz pozdější lekce.

### Vytvoření n-tice

Prázdná n-tice se vytvoří takto:

```
>>> x = ()
>>> type(x)
<class 'tuple'>
```

Pokud oddělíte nějaké hodnoty pomocí čárky, automaticky dostanete n-tici.

```
>>> 1, 2, 3
(1, 2, 3)
```

N-tici můžete také vytvořit takto:

```
>>> (1, 2, 3)
(1, 2, 3)
```

Pokud chcete vytvořit n-tici s jedinou hodnotou, musíte to udělat pomocí následujícího triku.

```
>>> 11
11
>>> 11,
(11,)
>>> (11,)
(11,)
```

#### Funkce tuple()

Jako argument předáváme této funkci sekvenci a ona ji konvertuje na n-tici. 

```
>>> tuple([1, 2, 3])
(1, 2, 3)
>>> tuple('abc')
('a', 'b', 'c')
```

> [note]
> Co se stane, když předáme jako parametr funkci tuple() jiže existující n-tici? Vyzkoušejte si to.