from ingrediente import Ingrediente
from pan import pan
from salchicha import salchicha
from acompañante import acompañante
from salsa import salsa
from topping import toppings
from hotdog import hotdog
import requests
import json

#Modulo de cargas
def cargar_api(menu, ingredientes):
    response_menu = requests.get(menu)
    response_ingrdientes = requests.get(ingredientes)
    menu = response_menu.json()
    ingredientes = response_ingrdientes.json()
    inventario = {}
    inventario = agregar_inicial(ingredientes,inventario)
    menu = []
    menu = hotdog_inicial(response_menu, inventario, menu)
    
def guardar(menu,inventario):
    guardar_menu = []
    guardar_inventario = []
    for x in menu:
        aux = vars(x)
        guardar_menu.append(aux)
    for y in inventario.keys():
        opciones = []
        for z in inventario[y]:
            temporal = vars(z)
            valor = temporal.pop("inventario")
            temporal["inventario"] = valor
            opciones.append(temporal)
        guardar_inventario.append({"Categoria":y,"Opciones":opciones})
    try:
        with open("menu.txt","w") as men:
            json.dump(guardar_menu,men)
        men.close()
        with open("ingredientes.txt","w") as ingr:
            json.dump(guardar_inventario,ingr)
        ingr.close()
        return True
        
    except:
        print("Error al guardar el archivo")
def cargar_archivo():
    menu_local = "menu.txt"
    Ingredientes_local = "ingredientes.txt"
    menu = []
    inventario = {}
    
    try:
        with open(Ingredientes_local, "r") as ingr:
            nuevo_inventario = json.load(ingr)
            agregar_inicial(nuevo_inventario,inventario)
        with open(menu_local, "r") as men:
            nuevo_menu = json.load(men)
            hotdog_inicial(nuevo_menu, inventario,menu)
    except:
        print("Error al cargar los archivos, se hará carga desde la api")
        #Recuerda poner la dirección de la api
        cargar_api()
            
#Modulo de ingredientes
def agregar_inicial(entrada, inventario):
    x = 0
    for clases in Ingrediente._subclasses_():
        if x > len(entrada):
            return False
        if clases._name_ == entrada[x]["Categoria"].lower():
                inventario[clases._name_] = []
                for y in entrada[x]["Opciones"]:
                    aux = clases(*y.values)
                    inventario[clases._name_].append(aux)
        x += 1
    return inventario
def productos_categoria(inventario, categoria = False):
    if not categoria:
        categoria = input("Introduzca con solo minúsculas la categoría que desea buscar----->").lower()
    try:
        for x in inventario[categoria]:
            x.mostrar()
    except:
        print("La categoría que ha introducido no existe")
        return False
    return inventario[categoria]
def productos_tipos(inventario):
    lista_categoria = productos_categoria(inventario)
    tipos = {}
    if lista_categoria:
        for x in lista_categoria:
            try:
                tipos[x.tipo].append(x.nombre)
            except:
                try:
                    tipos[x.tipo] = [x.nombre]
                except:
                    print("La categoría que introduciste no tiene tipo")
    else:
        return False
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
            for clases in Ingrediente._subclasses_():
                if clases._name_ == categoria:
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
#Modulo de inventarios
def ver_inventario(inventario):
    for x in inventario.values():
        for y in x:
            y.mostrar()
def buscar(inventario, nombre = False, categoria = False):
    if not categoria:
        productos = productos_categoria(inventario)
        if productos and not nombre:
            nombre = input("Introduce el nombre del producto que se debe buscar------>").lower()
            for x in productos:
                if x.nombre == nombre:
                    x.mostrar()
                else:
                    print("No se ha encontrado ningún producto con ese nombre")
        else:
            return False
    else:
        productos = productos_categoria(inventario, categoria)
        for x in productos:
            if x.nombre == nombre:
                return x
            else:
                return False
        
#Módulo de gestión de menú
def hotdog_inicial(entrada, inventario, menu):
    for x in entrada:
        aux = []
        for llave, valor in x.keys(), x.values():
            if llave.lower() != "toppings" and llave.lower() != "salsas":
                if llave.lower() == "nombre" and not buscar_menu(menu, valor.lower()):
                    
                    temporal = buscar(inventario, valor.lower(),llave.lower())
                    if temporal:
                        aux.append(temporal)
                        if temporal.inventario == 0:
                            print("Advertencia no hay disponibilidad en el inventario para este producto")
                    else:
                        print("El producto no se ha agregado porque sus ingredientes no existen en el inventario")
                        for y in inventario[llave.lower()]:
                            y.mostrar()
                        while True:
                            nuevo = input("Introduzca el nombre de otro ingrediente, en caso de no querer agregar el producto introduzca (NO)")
                            if nuevo == "NO":
                                return False
                            else:
                                temporal = buscar(inventario, nuevo,llave.lower())
                                if temporal:
                                    aux.append(temporal)
                                    break
                                else:
                                    print("No has introducido el nombre de un ingrediente existente, intenta de nuevo")
                else:
                    print("Ya existe una receta con ese nombre")
                    return False
            else:
                objetos = []
                for z in valor:
                    temporal = buscar(inventario, x.lower(),llave.lower())
                    if temporal:
                        objetos.append(temporal)
                        if temporal.inventario == 0:
                            print("Advertencia no hay disponibilidad en el inventario para este producto")
                    else:
                        print("El producto no se ha agregado porque sus ingredientes no existen en el inventario")
                        for y in inventario[llave.lower()]:
                            y.mostrar()
                        while True:
                            nuevo = input("Introduzca el nombre de otro ingrediente, en caso de no querer agregar el producto introduzca (NO)")
                            if nuevo == "NO":
                                return False
                            else:
                                temporal = buscar(inventario, nuevo,llave.lower())
                                if temporal:
                                    objetos.append(temporal)
                                    break
                                else:
                                    print("No has introducido el nombre de un ingrediente existente, intenta de nuevo")
                aux.append(objetos)
        if aux[1].tamaño == aux[2].tamaño:
            aux2 = aux[3]
            aux.pop(3)
            aux.append(aux2)
            receta = hotdog(*aux)
            menu.append(receta)
        else:
            while True:
                distintos = input("El tamaño del pan y de la salchicha no coinciden, si igual desea agregarlo introduzca (si), por el contrario si desea cancelar la operación introduzca (no)----->").lower()
                if distintos == "si":
                    aux2 = aux[3]
                    aux.pop(3)
                    aux.append(aux2)
                    receta = hotdog(*aux)
                    menu.append(receta)
                    break
                elif distintos == "no":
                    break
def agregar_hotdog(inventario, menu):
    diccio = {}
    diccio["nombre"] = input("Introduce el nombre del hot dog---->").lower()
    diccio["pan"] = input("Introduce el nombre del pan-------->").lower()
    diccio["salchicha"] = input("Introduce el nombre de la salchicha------>").lower()
    lostoppings = []
    while True:
        decision = input("""Introduce (si) si quieres agregar un topping o un nuevo topping
                        Introduce (no) si no quieres ningún topping o si ya no quieres más toppings
                        ----->""")
        if decision == "si":
            topping = input("Introduce el nombre del topping").lower()
            lostoppings.append(topping)
        elif decision == "no":
            break
        else:
            print("Has introducido una opción inválida")
    diccio["toppings"] = lostoppings
    lassalsas = []
    while True:
        decision = input("""Introduce (si) si quieres agregar una salsa o una nueva salsa
                        Introduce (no) si no quieres ninguna salsa o si ya no quieres más salsas
                        ----->""")
        if decision == "si":
            sals = input("Introduce el nombre de la salsa").lower()
            lassalsas.append(sals)
        elif decision == "no":
            break
        else:
            print("Has introducido una opción inválida")
    diccio["salsas"] = lassalsas
    diccio["acompañante"] = input("Introduce el nombre del acompañante").lower()
    
    transicion = [diccio]
    hotdog_inicial(transicion,inventario,menu)
    
def buscar_menu(menu, nombre= False):
    if nombre:
        for x in menu:
            if x.nombre == nombre:
                return x
        return False
    nombre = input("Introduce el nombre de la receta a buscar----->")
    for x in menu:
        if x.nombre == nombre:
            return x

    print("No se ha encontrado ninguna receta con ese nombre")
    return False
def ver_menu(menu):
    for x in menu:
        x.mostrar()
def eliminar(menu, inventario, nombre = False):
    if nombre:
        for x in menu:
            if x.nombre == nombre:
                menu.remove(x)
                return True
        return False
    
    nombre = input("Introduce el nombre de la receta a eliminar----->")
    for x in menu:
        if x.nombre == nombre:
            if not x.comprobar_inventario():
                menu.remove(x)
                return True
            while True:
                comprobar = input("""El hot dog que deseas eliminar aún tiene todos sus ingredientes disponibles en el inventario.
                                  Si aun deseas eliminarlo introduce (si)
                                  Si deseas conservarlo introduce (no)
                                  ----->""").lower()
                if comprobar == "si":
                    menu.remove(x)
                    return True
                elif comprobar == "no":
                    return False
                else:
                    print("No has introducido una opción válida")
                
        else:
            print("No se ha encontrado ninguna receta con ese nombre")
            return False