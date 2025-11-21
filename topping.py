from ingrediente import Ingrediente
#clase topping, clase hija de ingrediente
class toppings(Ingrediente):
    def __init__(self, nombre, tipo, presentación, inventario = 0):
        super().__init__(nombre, inventario)
        self.tipo = tipo
        self.presentación = presentación