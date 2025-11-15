from ingrediente import Ingrediente
class salsa(Ingrediente):
    def __init__(self, nombre, base, color, inventario = 0):
        super().__init__(inventario, nombre)
        self.base = base
        self.color = color