from ingrediente import Ingrediente
from pan import pan
from salchicha import salchicha
from acompañante import acompañante
from salsa import salsa
from topping import toppings
aux = pan()
#Modulo de ingredientes
def agregar_inicial(entrada):
    inventario = {}
    x = 0
    for clases in Ingrediente.__subclasses__():
        if x > len(entrada):
            return False
        if clases.__name__ == entrada[x]["Categoria"].lower():
                inventario[clases.__name__] = []
                for y in entrada[x]["Opciones"]:
                    aux = clases(*y.values)
                    inventario[clases.__name__].append(aux)
        x += 1
    return inventario
def productos_categoria(inventario):
    categoria = input("Introduzca con solo minúsculas la categoría que desea buscar----->").lower()
    try:
        inventario[categoria].mostrar()
    except:
        print("La categoría que ha introducido no existe")
    return inventario[categoria]
def productos_tipos(inventario):
    lista_categoria = productos_categoria(inventario)
    tipos = {}
    for x in lista_categoria:
        try:
            tipos[x.tipo].append(x.nombre)
        except:
            try:
                tipos[x.tipo] = [x.nombre]
            except:
                print("La categoría que introduciste no tiene tipo")
def agregar(inventario):
    categoria = input("Introduzca la categoria del producto----->").lower()
    try:
        aux = inventario[categoria]
    except:
        print("La categoría que ha introducido no existe")
        return False
    nombre = input("Introduce el nombre del producto a agregar------>").lower()
    for x in aux:
        if x.nombre == nombre:
            while True:
                cantidad = input("El producto que deseas agregar ya existe, indica en números la cantidad de ese producto que deseas agregar----->")
                if cantidad.isnumeric():
                    x.cantidad += int(cantidad)
                    break
                else:
                    print("Has introducido un caracter inválido, intentalo de nuevo")
        else:
            necesarios = list(vars(x).keys())
            necesarios.pop(0)
            nuevo = [nombre]
            for y in range(len(necesarios)):
                necesarios[y]= input(f"Introduce el/la {necesarios[y]} del producto")
            temporal = necesarios[0]
            necesarios.pop(0)
            necesarios.append(temporal)
            nuevo.extend(necesarios)
            for clases in Ingrediente.__subclasses__():
                if clases.__name__ == categoria:
                    aux2 = clases(*nuevo)
                    inventario[categoria].append(aux2)
                    return True
                
def eliminar(inventario, menu):
    categoria = input("Introduzca la categoria del producto----->").lower()
    try:
        aux = inventario[categoria]
    except:
        print("La categoría que ha introducido no existe")
        return False
    nombre = input("Introduce el nombre del producto a agregar------>").lower()
    for x in inventario[categoria]:
        if x.nombre == nombre:
            if(x.eliminando(menu)):
                print("Ingredientes y recetas eliminadas con éxito")
                inventario[categoria].remove(x)
                return True
            else:
                print("El ingrediente no fue eliminado") 
               
                