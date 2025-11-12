class hola:
    def __init__(self, hola, adios):
        self.hola = hola
        self.adios = adios
aux = hola("si","no")
aux2 = list(vars(aux).keys())

print(aux2)