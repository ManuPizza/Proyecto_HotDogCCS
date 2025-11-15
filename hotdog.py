class hotdog():
    def __init__(self,nombre, pan, salchicha, toppings, salsas, acompañante):
        self.nombre = nombre
        self.pan = pan
        self.salchicha = salchicha
        self.toppings = toppings
        self.salsas = salsas
        self.acompañante = acompañante
    def mostrar(self):
        topping = []
        salsa = []
        if self.toppings:
            for x in self.toppings:
                topping.append(x.nombre)
        if self.salsas:
            for y in self.salsas:
                salsa.append(y.nombre)
        print(f"""Nombre: {self.nombre}
              Pan: {self.pan.nombre}
              Salchicha: {self.salchicha.nombre}
              Toppings: {topping}
              Salsas: {salsa}
              """)
        if self.acompañante:
            print(f"Acompañante{self.acompañante.nombre}")
    def comprobar_inventario(self):
        if self.pan.inventario == 0 or self.salchicha.inventario == 0 or self.acompañante.inventario == 0:
            return False
        for x in self.salsas:
            if x.inventario == 0:
                return False
        for y in self.toppings:
            if y.inventario == 0:
                return False
        return True
prueba = hotdog("hola", "adios", "pr", [], [], "zt")

kiko = vars(prueba)
print(kiko)