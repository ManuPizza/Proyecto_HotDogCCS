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
              Salsas: {salsa}""")
        if self.acompañante:
            print(f"              Acompañante: {self.acompañante.nombre}")
    def comprobar_inventario(self):
        if self.pan.inventario == 0 or self.salchicha.inventario == 0 or self.acompañante.inventario == 0:
            return False
        if self.salsas:
            for x in self.salsas:
                if x.inventario == 0:
                    return False
        if self.toppings:
            for y in self.toppings:
                if y.inventario == 0:
                    return False
        return True
    def comprobar_disponibilidad(self):
        total = []
        if self.salsas:
            if len(self.salsas) > 1:
                if self.salsas[0].inventario > 0:    
                    for x in range(1,len(self.salsas)):
                        if self.salsas[x].inventario == 0:
                            return False
                        elif self.salsas[x].inventario >= self.salsas[x-1].inventario:
                            total.append(self.salsas[x].inventario)
            else:
                total.append(self.salsas[0].inventario)
        if self.toppings:
            if len(self.toppings) > 1:
                if self.toppings[0].inventario > 0:    
                    for x in range(1,len(self.toppings)):
                        if self.toppings[x].inventario == 0:
                            return False
                        elif self.toppings[x].inventario >= self.toppings[x-1].inventario:
                            total.append(self.toppings[x].inventario)
            else:
                total.append(self.toppings[0].inventario)
        if self.acompañante:
            if self.pan.inventario == self.salchicha.inventario == self.acompañante.inventario and self.pan.inventario != 0:
                total.extend([self.pan.inventario,self.salchicha.inventario,self.acompañante.inventario])
        else:
            if self.pan.inventario == self.salchicha.inventario and self.pan.inventario != 0:
                total.extend([self.pan.inventario,self.salchicha.inventario])
        if total:
            posibilidad = min(total)
            return posibilidad
        else:
            return False
    def maximo_dia(self):
        total = self.comprobar_disponibilidad()
        if total:
            if self.salsas:
                for x in self.salsas:
                    x.inventario -= total
            if self.toppings:
                for y in self.toppings:
                    y.inventario-= total
            if self.acompañante:
                self.acompañante.inventario -= total
            self.pan.inventario-= total
            self.salchicha-=total
            return True
        else:
            return False
    def comprar(self):
        if self.comprobar_inventario:
            self.pan.inventario -= 1
            self.salchicha.inventario -= 1
            if self.acompañante:
                self.acompañante.inventario -= 1
            if self.salsas:
                for x in self.salsas:
                    x.inventario -=1
            if self.toppings:
                for y in self.toppings:
                    y.inventario -=1
            return True
        else:
            return False
    def compra_fallida(self):
        ingredientes = []
        if self.pan.inventario == 0:
            ingredientes.append(self.pan.nombre)
        if self.salchicha.inventario == 0:
            ingredientes.append(self.salchicha.nombre)
        if self.acompañante:
            if self.acompañante.inventario == 0:
                ingredientes.append(self.acompañante.nombre)
        if self.salsas:
                for x in self.salsas:
                    if x.inventario == 0:
                        ingredientes.append(x.nombre)
        if self.toppings:
                for y in self.toppings:
                    if y.inventario == 0:
                        ingredientes.append(y.nombre)
        return self.nombre, ingredientes