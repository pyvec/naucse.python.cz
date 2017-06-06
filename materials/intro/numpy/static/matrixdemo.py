import numpy

with open('python-logo-template.svg') as f:
    template = f.read()

class MatrixDemo:
    def __init__(self, m=numpy.eye(3)):
        self.matrix = m[:2, :3].reshape(6)

    def _repr_svg_(self):
        return template.format(*self.matrix)
