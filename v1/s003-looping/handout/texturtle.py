import contextlib

import turtle

@contextlib.contextmanager
def ctx():
    print(r'\turtle{', end='')
    turtle.speed(-1)
    yield
    print('}')
    turtle.exitonclick()


def forward(n):
    turtle.forward(n)
    print('fd=%s' % n, end=',')

def left(n):
    turtle.left(n)
    print('lt=%s' % n, end=',')

def right(n):
    turtle.right(n)
    print('rt=%s' % n, end=',')
