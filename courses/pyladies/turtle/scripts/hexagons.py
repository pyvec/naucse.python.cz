from turtle import forward, left, right, penup, pendown

uhel = 180 - 180 * (1 - 2/6)
vzdalenost = 50
print(uhel)

for sestiuhel in range(6):
    for strana in range(6):
        forward(vzdalenost)
        left(uhel)
    right(uhel * 1)
    penup()
    forward(vzdalenost * 2)
    pendown()
    left(uhel * 2)

input()
