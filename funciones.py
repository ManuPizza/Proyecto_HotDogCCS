from ingrediente import Ingrediente
from pan import pan
from salchicha import salchicha
from acompañante import acompañante
from salsa import salsa
from topping import toppings
from hotdog import hotdog
import requests
import json
import random
import copy
import os
#Modulo de cargas
def cargar_api(api_menu, api_ingredientes):
    response_menu = requests.get(api_menu)
    response_ingrdientes = requests.get(api_ingredientes)
    menus = response_menu.json()
    ingredientes = response_ingrdientes.json()
    inventario = {}
    inventario = agregar_inicial(ingredientes,inventario)
    menu = []
    menu = hotdog_inicial(menus, inventario, menu)
    return menu, inventario
    
def guardar(menu,inventario):
    guardar_menu = []
    guardar_inventario = []
    for x in menu:
        aux = vars(x)
        #Se me olvidó cambiar los objetos de las clases a objetos guardables en json
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
def cargar_archivo(api_menu, api_ingredientes):
    menu_local = "menu.txt"
    Ingredientes_local = "ingredientes.txt"
    menu = []
    inventario = {}
    if os.path.exists(Ingredientes_local) and os.path.exists(menu_local):
        try:
            with open(Ingredientes_local, "r") as ingr:
                nuevo_inventario = json.load(ingr)
                agregar_inicial(nuevo_inventario,inventario)
            with open(menu_local, "r") as men:
                nuevo_menu = json.load(men)
                hotdog_inicial(nuevo_menu, inventario,menu)
            return menu, inventario
        except:
            print("Error al cargar los archivos, se hará carga desde la api")
            return cargar_api(api_menu, api_ingredientes)
    else:
        print("Esta es la primera carga")
        return cargar_api(api_menu,api_ingredientes)
        
            
#Modulo de ingredientes
def agregar_inicial(entrada, inventario):
    x = 0
    for clases in Ingrediente.__subclasses__():
        if x > len(entrada):
            return False
        if clases.__name__ == entrada[x]["Categoria"].lower():
                inventario[clases.__name__] = []
                for y in entrada[x]["Opciones"]:
                    aux = clases(*[valor.lower() if isinstance(valor, str) else valor for valor in y.values()])
                    inventario[clases.__name__].append(aux)
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
        return tipos    
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
        if x.nombre.lower() == nombre.lower():
            while True:
                cantidad = input("El producto que deseas agregar ya existe, indica en números la cantidad de ese producto que deseas agregar----->")
                if cantidad.isnumeric() and int(cantidad)>= 1:
                    cantidad = int(cantidad)
                    x.inventario += cantidad
                    return True
                else:
                    print("Has introducido un caracter inválido, intentalo de nuevo")
        
    necesarios = list(vars(x).keys())
    necesarios.pop(0)
    nuevo = [nombre]
    for y in range(len(necesarios)):
        if necesarios[y] != "inventario" and necesarios[y] != "tamaño":    
            necesarios[y]= input(f"Introduce el/la {necesarios[y]} del producto------>")
        else:
            while True:
                necesarios[y]= input(f"Introduce el/la {necesarios[y]} del producto------>")
                if necesarios[y].isnumeric() and int(necesarios[y])>= 1:
                    necesarios[y] = int(necesarios[y])
                    break
                else:
                    print("solo puedes introducir números y deben ser iguales o mayores que 1")
    temporal = necesarios[0]
    necesarios.pop(0)
    necesarios.append(temporal)
    nuevo.extend(necesarios)
    for clases in Ingrediente.__subclasses__():
        if clases.__name__ == categoria:
            aux2 = clases(*nuevo)
            inventario[categoria].append(aux2)
            return True
                
def eliminar_inventario(inventario, menu):
    categoria = input("Introduzca la categoria del producto----->").lower()
    try:
        aux = inventario[categoria]
    except:
        print("La categoría que ha introducido no existe")
        return False
    nombre = input("Introduce el nombre del producto a eliminar------>").lower()
    for x in inventario[categoria]:
        if x.nombre == nombre:
            if(x.eliminando(menu, inventario[categoria])):
                print("Ingredientes y recetas eliminadas con éxito")
                return True
            else:
                print("El ingrediente no fue eliminado") 
#Modulo de inventarios
def ver_inventario(inventario):
    for x in inventario.values():
        for y in x:
            y.mostrar()
def buscar(inventario, nombre = False, categoria = False):
    aux = False
    if not categoria:
        productos = productos_categoria(inventario)
        if productos and not nombre:
            nombre = input("Introduce el nombre del producto que se debe buscar------>").lower()
            for x in productos:
                if x.nombre == nombre:
                    x.mostrar()
                    aux = True
                    break   
            if not aux:     
                print("No se ha encontrado ningún producto con ese nombre")
        else:
            return False
    else:
        productos = productos_categoria(inventario, categoria)
        for x in productos:
            if x.nombre == nombre:
                return x
            
        return False
        
#Módulo de gestión de menú
def hotdog_inicial(entrada, inventario, menu):
    for x in entrada:
        aux = []
        for llave, valor in x.items():
            if llave.lower() != "toppings" and llave.lower() != "salsas":
                if llave.lower() == "nombre" and buscar_menu(menu, valor.lower()):
                    print("Ya existe una receta con ese nombre")
                    return False
                elif llave.lower() == "nombre":
                    nombre = valor.lower()
                else:
                    if not valor:
                        aux.append(None)
                    else:
                        
                        if llave.lower() != "nombre" and not buscar_menu(menu, valor.lower()):
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
                                    nuevo = input("Introduzca el nombre de otro ingrediente, en caso de no querer agregar el producto introduzca (no)").lower()
                                    if nuevo == "no":
                                        return False
                                    else:
                                        temporal = buscar(inventario, nuevo,llave.lower())
                                        if temporal:
                                            aux.append(temporal)
                                            break
                                        else:
                                            print("No has introducido el nombre de un ingrediente existente, intenta de nuevo")
            else:
                objetos = []
                errando = llave.lower()
                if llave.lower() == "salsas":
                    errando = "salsa"
                for z in valor:
                    temporal = buscar(inventario, z.lower(),errando)
                    if temporal:
                        objetos.append(temporal)
                        if temporal.inventario == 0:
                            print("Advertencia no hay disponibilidad en el inventario para este producto")
                    else:
                        print("El producto no se ha agregado porque sus ingredientes no existen en el inventario")
                        for y in inventario[errando]:
                            y.mostrar()
                        while True:
                            nuevo = input("Introduzca el nombre de otro ingrediente, en caso de no querer agregar el producto introduzca (NO)")
                            if nuevo == "NO":
                                return False
                            else:
                                temporal = buscar(inventario, nuevo,errando)
                                if temporal:
                                    objetos.append(temporal)
                                    break
                                else:
                                    print("No has introducido el nombre de un ingrediente existente, intenta de nuevo")
                aux.append(objetos)
        if aux[0].tamaño == aux[1].tamaño:
            aux.insert(0,nombre)
            receta = hotdog(*aux)
            menu.append(receta)
        else:
            while True:
                distintos = input("El tamaño del pan y de la salchicha no coinciden, si igual desea agregarlo introduzca (si), por el contrario si desea cancelar la operación introduzca (no)----->").lower()
                if distintos == "si":
                    aux.insert(0,nombre)
                    receta = hotdog(*aux)
                    menu.append(receta)
                    break
                elif distintos == "no":
                    break
    return menu
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
            topping = input("Introduce el nombre del topping------>").lower()
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
            sals = input("Introduce el nombre de la salsa----->").lower()
            lassalsas.append(sals)
        elif decision == "no":
            break
        else:
            print("Has introducido una opción inválida")
    diccio["salsas"] = lassalsas
    diccio["acompañante"] = input("Introduce el nombre del acompañante------>").lower()
    
    transicion = [{"nombre":diccio["nombre"],"pan": diccio["pan"], "salchicha": diccio["salchicha"], "toppings": diccio["toppings"], "salsas":diccio["salsas"],"acompañante":diccio["acompañante"]}]
    hotdog_inicial(transicion,inventario,menu)
    
def buscar_menu(menu, nombre= False):
    if nombre:
        for x in menu:
            if x.nombre == nombre:
                return x
        return False
    nombre = input("Introduce el nombre de la receta a buscar----->").lower()
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
        
#Modulo de simulación de ventas
def confirmar_disponibilidad(menu, inventario):
    guardar_inventario = copy.deepcopy(inventario)
    guardar_menu = copy.deepcopy(menu)
    total = 0
    for x in menu:
        if x.maximo_dia():
            total +=1
    if total >= 1000:
        inventario = guardar_inventario
        menu = guardar_menu
        return True
    else:
        while True:
            decision = input(f"""¿Está seguro que desea simular el día? El total de hot dogs disponibles para la venta es {total}
                             El mínimo debe ser 1000
                             Introduzca (si) si desea continuar con la simulación
                             Introduzca (no) si desea detener la simulacion
                             -------->""").lower()
            if decision == "si":
                inventario = guardar_inventario
                menu = guardar_menu
                return True
            elif decision == "no":
                break
            else:
                print("Por favor solo introduce (si) o (no)")

def simular_dia(menu, inventario):
    opinion = 0
    no = 0
    vendidos = 0
    mas_vendido = {}
    no_hotdog = []
    no_ingrediente = []
    acompañante_vendido = []
    if confirmar_disponibilidad(menu,inventario):
        clientes = random.randint(0,200)
        hotdogs_vendidos = 0
        for i in range(clientes):
            pedido = random.randint(0,5)
            hotdogs_vendidos += pedido
            if pedido == 0:
                print(f"El cliente numero {i} cambió de opinión")
                opinion+= 1
            else:
                lista_pedidos = []
                lista_fallidos = []
                for x in range(pedido):
                    seleecionado = random.choice(menu)
                    if seleecionado.comprar():
                        lista_pedidos.append(seleecionado.nombre)
                        vendidos += 1
                        if seleecionado.acompañante:
                            if seleecionado.acompañante.nombre not in acompañante_vendido:
                                acompañante_vendido.append(seleecionado.acompañante.nombre)
                        try:
                            mas_vendido[seleecionado.nombre] += 1
                        except:
                            mas_vendido[seleecionado] = 1
                    else:
                        falla= seleecionado.compra_fallida()
                        fallido = falla[0]
                        motivos = falla[1]
                        if fallido not in lista_fallidos:
                            lista_fallidos.append(fallido)
                            if fallido not in no_hotdog:
                                no_hotdog.append(fallido)
                if lista_pedidos:
                    print(f"El cliente {i} compro: ")
                    for x in lista_pedidos:
                        print(x)
                    try:
                        if motivos:
                            print(f"Ademas el cliente {i} no pudo comprar estos productos: {lista_fallidos} debido a la falta de los siguientes ingredientes:")
                            for y in motivos:
                                print(y)
                                if y not in no_ingrediente:
                                    no_ingrediente.append(y)
                        if random.choice([True,False]):
                            extra = False
                            maximo = 0
                            while not extra and maximo<50:
                                extra = random.choice(inventario["acompañante"])
                                if extra.inventario == 0:
                                    extra = False
                                    maximo+=1
                            print(f"El cliente {i} compro un acompañante adicional: {extra.nombre}")
                            if extra.nombre not in acompañante_vendido:
                                acompañante_vendido.append(extra.nombre)
                    except:
                        print("No hay inventario para ninguna venta")
                else:
                    print(f"El cliente {i} no pudo comprar estos productos: {lista_fallidos} debido a la falta de los siguientes productos:")
                    for x in motivos:
                        print(x)
                    no += 1
                
    total = clientes - no
    promedio = total / vendidos
    mayor = max(mas_vendido.values())
    mejores_vendidos = [key for key,value in mas_vendido.items() if value == mayor]
    print(f"El numero de clientes que cambiaron de opinión fue: {opinion}")
    print(f"El numero de clientes que no pudieron comprar fue: {no}")
    print(f"El total de clientes fue: {total}")
    print(f"El promedio de hotdogs por clientes fue: {promedio}")
    print(f"El o los hotdogs más vendidos fueron: {mejores_vendidos}")
    print(f"Los hotdogs que causaron que el cliente se fuese sin comprar nada fueron: {no_hotdog}")
    print(f"Los ingredientes que causaron que el cliente se fuese sin comprar nada fueron: {no_ingrediente}")
    print(f"Los acompañantes vendidos fueron: {acompañante_vendido}")

                    
            
                    