from ingrediente import Ingrediente
class toppings(Ingrediente):
    def __init__(self, nombre, tipo, presentación, inventario = 0):
        super().__init__(inventario, nombre)
        self.tipo = tipo
        self.presentación = presentación