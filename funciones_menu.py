from colorama import Fore, Style
from tabulate import tabulate
from gestionar_productos_bd import (gestionar_producto, normalizar_texto_bd)
import re

# Función para agregar un producto
def agregar_producto(conn, cursor):
    """
    Permite agregar productos a la base de datos.
    No permite ingresar números ni caracteres especiales al elegir el nombre o la marca del producto. Lanza mensaje de error. Solo permite ingresar "ñ" y vocales con tildes.
    Elimina espacios adicionales que pueda ingresar adicionalmente el usuario. Si ingresa mayúsculas, lo convierte a minúscula y elimina tildes antes de guardarlo en la base de datos.
    No permite ingresar letras ni caracteres especiales al elegir la cantidad. Solo números enteros.
    Si el producto ya estaba registrado anteriormente, suma la cantidad nueva a la cantidad que ya existía.
    """
    while True:
        # NOMBRE
        nombre = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
            f"{Fore.WHITE}{Style.BRIGHT}Ingresá el nombre del producto: " 
            f"{Style.BRIGHT}{Fore.YELLOW}")
        nombre = nombre.strip().lower()  # Elimina espacios y lo convierte a minúscula

        if nombre == '':  # Si el usuario presiona Enter (cadena vacía)
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
            return  # Regresa al menú principal

        while True:  # Valida que el nombre del producto no contenga números ni caracteres especiales
            if re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", nombre):
                break  # Sale del bucle si el nombre es válido
            print(f"{Fore.RED}{Style.BRIGHT}El nombre no puede contener números ni caracteres especiales.\n")
            nombre = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
                f"{Style.BRIGHT}Ingresá el nombre del producto: " 
                f"{Style.BRIGHT}{Fore.YELLOW}")
            nombre = nombre.strip().lower()

            if nombre == '':
                print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
                return

        # MARCA
        marca = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
            f"{Style.BRIGHT}Ingresá la marca del producto: " 
            f"{Style.BRIGHT}{Fore.YELLOW}")
        marca = marca.strip().lower()

        if marca == '':
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
            return

        while True:
            if re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", marca):
                break
            print(f"{Fore.RED}{Style.BRIGHT}La marca no puede contener números ni caracteres especiales.\n")
            marca = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
                f"{Style.BRIGHT}Ingresá la marca del producto: " 
                f"{Style.BRIGHT}{Fore.YELLOW}")
            marca = marca.strip().lower()

            if marca == '':
                print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
                return

        # CANTIDAD
        cantidad = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
            f"{Style.BRIGHT}Ingresá la cantidad del producto: " 
            f"{Style.BRIGHT}{Fore.YELLOW}")

        if cantidad == '':
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
            return

        while not cantidad.isdigit():
            print(f"{Fore.RED}{Style.BRIGHT}Cantidad no válida. Asegurate de ingresar un número entero.\n")
            cantidad = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
                f"{Style.BRIGHT}Ingresá la cantidad del producto: " 
                f"{Style.BRIGHT}{Fore.YELLOW}")

            if cantidad == '':
                print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
                return

        cantidad = int(cantidad)
        gestionar_producto(conn, cursor, nombre=nombre, marca=marca, cantidad=cantidad, operacion="agregar_cantidad")

# Función para modificar los productos de la base de datos
def modificar_producto_bd(conn, cursor):
    """
    Le consulta al usuario el ID del producto a modificar. Lanza mensajes de error si ingresa un input que no sea un número
    Si no hay productos registrados en la base de datos, le avisa al usuario y ofrece la opción de agregar productos.
    Brinda la opción de modificar el nombre, la marca, la cantidad, volver a la consulta de ID o volver al menú principal.
    Rechaza los nombres y las marcas con caracteres especiales y números.
    Permite ingresar tildes, "ñ" y mayúsculas pero guarda la información en la base de datos sin tildes y en minúscula.
    """
    # Verifica si existen productos en la base de datos
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    if total_productos == 0:
        print(f"{Fore.RED}{Style.BRIGHT}No hay productos registrados en el inventario.\n")
        # Pregunta al usuario si desea agregar un producto
        opcion = input(f"{Fore.WHITE}{Style.BRIGHT}¿Querés agregar un producto?\n"
                       f"Ingresá 's' para agregar un producto o presioná 'Enter' para volver al menú principal: ").strip().lower()
        if opcion == "s":
            agregar_producto(conn, cursor)  # Llama a la función para agregar productos
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
        return  # Termina la función si no hay productos

    while True:
        while True:
            id_producto = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
                                f"{Style.BRIGHT}{Fore.WHITE}Ingresá el ID del producto a modificar: {Fore.YELLOW}").strip()
            if not id_producto:
                print(f"{Fore.BLUE}{Style.BRIGHT}Operación cancelada.\nVolviendo al menú principal...")
                return
            if not id_producto.isdigit():
                print(f"{Fore.RED}El ID debe ser un número entero.\n")
                continue
            id_producto = int(id_producto)

            cursor.execute("SELECT id, nombre, marca, cantidad FROM productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()

            if producto:
                break
            else:
                print(f"{Fore.RED}{Style.BRIGHT}El producto consultado no existe. Intentá de nuevo.\n")

        while True:
            print(f"{Fore.GREEN}{Style.BRIGHT}Producto encontrado: ID: '{producto[0]}' - Nombre: '{producto[1]}' - Marca: '{producto[2]}' - Cantidad actual: '{producto[3]}'")
            print(f"{Style.BRIGHT}\n¿Qué te gustaría modificar?")
            print("1. Nombre")
            print("2. Marca")
            print("3. Cantidad")
            print("4. Volver a la consulta de ID")
            print("0. Volver al menú principal\n")

            opcion = input(f"{Fore.WHITE}{Style.BRIGHT}Seleccioná una opción: {Fore.YELLOW}{Style.BRIGHT}").strip()

            if opcion == '1':  # Modificar nombre
                while True:
                    nuevo_nombre = input(f"{Fore.WHITE}{Style.NORMAL}\nPresioná {Style.BRIGHT}'Enter'{Style.NORMAL} para ir atrás.\n"
                                         f"{Fore.WHITE}{Style.BRIGHT}Ingresá el nuevo nombre para el producto '{producto[1]}': {Fore.YELLOW}").strip()
                    if not nuevo_nombre:
                        print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo atrás...\n")
                        break
                    if not normalizar_texto_bd(nuevo_nombre).replace(" ", "").isalpha():  # Valida que solo contenga letras y espacios
                        print(f"{Fore.RED}{Style.BRIGHT}El nombre no puede contener números ni caracteres especiales.")
                        continue
                    gestionar_producto(conn, cursor, id_producto=id_producto, nombre=nuevo_nombre, operacion="actualizar")
                    print(f"{Fore.GREEN}{Style.BRIGHT}Nombre del producto actualizado a '{normalizar_texto_bd(nuevo_nombre)}'.\n")
                    break

            elif opcion == '2':  # Modificar marca
                while True:
                    nueva_marca = input(f"{Fore.WHITE}{Style.NORMAL}\nPresioná {Style.BRIGHT}'Enter'{Style.NORMAL} para ir atrás.\n"
                                        f"{Fore.WHITE}{Style.BRIGHT}Ingresá la nueva marca para el producto '{producto[2]}': {Fore.YELLOW}").strip()
                    if not nueva_marca:
                        print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo atrás...\n")
                        break
                    if not all(c.isalpha() or c == ' ' for c in nueva_marca):  # Valida solo letras y espacios
                        print(f"{Fore.RED}{Style.BRIGHT}La marca no puede contener números ni caracteres especiales.")
                        continue
                    nueva_marca_normalizada = normalizar_texto_bd(nueva_marca)
                    gestionar_producto(conn, cursor, id_producto=id_producto, marca=nueva_marca_normalizada, operacion="actualizar")
                    print(f"{Fore.GREEN}{Style.BRIGHT}Marca del producto actualizada a '{nueva_marca_normalizada}'.\n")
                    break

            elif opcion == '3':  # Modifica cantidad
                nueva_cantidad = input(f"{Fore.WHITE}{Style.NORMAL}\nPresioná {Style.BRIGHT}'Enter'{Style.NORMAL} para ir atrás.\n"
                                       f"{Fore.WHITE}{Style.BRIGHT}Ingresá la nueva cantidad para el producto '{producto[1]}' - '{producto[2]}': {Fore.YELLOW}").strip()
                if not nueva_cantidad:  # Permite regresar atrás
                    print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo atrás...\n")
                    continue
                if nueva_cantidad.isdigit():
                    gestionar_producto(conn, cursor, id_producto=id_producto, cantidad=int(nueva_cantidad), operacion="actualizar")
                    print(f"{Fore.GREEN}{Style.BRIGHT}Cantidad del producto actualizada a {nueva_cantidad}.\n")
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}Cantidad no válida. Debe ser un número entero.\n")
                    continue

            elif opcion == '4':  # Vuelve a la consulta de ID
                print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo a la consulta de ID...\n")
                break

            elif opcion == '0':  # Vuelve al menú principal
                print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
                return

            else:
                print(f"{Fore.RED}{Style.BRIGHT}Opción no válida. Seleccioná una de las opciones.")

            # Actualiza los datos del producto en caso de cambios
            cursor.execute("SELECT id, nombre, marca, cantidad FROM productos WHERE id = ?", (id_producto,))
            producto = cursor.fetchone()

# Función para buscar productos de la base de datos
def buscar_producto(conn, cursor):
    """
    Permite buscar los productos de la base de datos por ID, nombre o marca.
    Si no hay productos registrados en el inventario, ofrece la opción de agregar productos.
    La búsqueda no distingue entre mayúsculas y minúsculas (case insensitive).
    Brinda la opción de ver todos los productos, volver atrás y volver al menú principal.
    """
    # Verifica si hay productos en la base de datos
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    if total_productos == 0:
        print(f"{Fore.RED}{Style.BRIGHT}No hay productos registrados en el inventario.\n")
        # Pregunta al usuario si desea agregar un producto
        opcion = input(f"{Fore.WHITE}{Style.BRIGHT}¿Querés agregar un producto?\n"
                       f"Ingresá 's' para agregar un producto o presioná 'Enter' para volver al menú principal: ").strip().lower()
        if opcion == "s":
            agregar_producto(conn, cursor)  # Usa la función para agregar productos
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
        return  # Termina la función si no hay productos

    # Menú de búsqueda
    while True:
        print(f"{Style.BRIGHT}{Fore.WHITE}\nBuscar producto{Style.RESET_ALL}")
        print("1. Buscar por ID")
        print("2. Buscar por nombre")
        print("3. Buscar por marca")
        print("4. Ver todos los productos")
        print("0. Volver al menú principal")
        
        opcion = input(f"{Fore.WHITE}{Style.BRIGHT}\nSeleccioná una opción: {Fore.YELLOW}").strip()

        if opcion == '1':
            id_producto = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
                                 f"{Fore.WHITE}{Style.BRIGHT}Ingresa el ID del producto: {Fore.YELLOW}").strip()
            if id_producto == '':  # Si el usuario presiona Enter, vuelve al menú de búsqueda
                continue
            if id_producto.isdigit():
                cursor.execute("SELECT * FROM productos WHERE id=?", (id_producto,))
                resultado = cursor.fetchone()
                if resultado:
                    print(Fore.WHITE + Style.NORMAL + tabulate([resultado], headers=["ID", "Nombre", "Marca", "Cantidad"], tablefmt="simple_grid"))
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}No existe un producto con el ID ingresado.")
            else:
                print(f"{Fore.RED}{Style.BRIGHT}El ID debe ser un número.")
        
        elif opcion == '2':
            nombre_producto = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
                                     f"{Fore.WHITE}{Style.BRIGHT}Ingresa el nombre del producto: {Fore.YELLOW}").strip().lower()
            if nombre_producto == '':  # Si el usuario presiona Enter, vuelve al menú de búsqueda
                continue
            nombre_producto_normalizado = normalizar_texto_bd(nombre_producto)  # Normaliza el nombre ingresado
            
            cursor.execute("SELECT * FROM productos")
            resultados = cursor.fetchall()
            
            # Filtra los resultados normalizando los nombres en la base de datos
            productos_filtrados = [
                producto for producto in resultados 
                if nombre_producto_normalizado in normalizar_texto_bd(producto[1].lower())
            ]
            
            if productos_filtrados:
                print(Fore.WHITE + Style.NORMAL + tabulate(productos_filtrados, headers=["ID", "Nombre", "Marca", "Cantidad"], tablefmt="simple_grid"))
            else:
                print(f"{Fore.RED}{Style.BRIGHT}No existe ningún producto con el nombre ingresado.")
        
        elif opcion == '3':
            marca_producto = input(f"{Fore.WHITE}{Style.NORMAL}Presioná {Style.BRIGHT}'Enter'{Style.NORMAL} para volver al menú principal.\n"
                                    f"{Fore.WHITE}{Style.BRIGHT}Ingresa la marca del producto: {Fore.YELLOW}").strip().lower()
            if marca_producto == '':  # Si el usuario presiona Enter, vuelve al menú de búsqueda
                continue
            marca_producto_normalizada = normalizar_texto_bd(marca_producto)  # Normaliza la marca ingresada
            
            cursor.execute("SELECT * FROM productos")
            resultados = cursor.fetchall()
            
            # Filtra los resultados normalizando las marcas en la base de datos
            productos_filtrados = [
                producto for producto in resultados 
                if marca_producto_normalizada in normalizar_texto_bd(producto[2].lower())
            ]
            
            if productos_filtrados:
                print(Fore.WHITE + Style.NORMAL + tabulate(productos_filtrados, headers=["ID", "Nombre", "Marca", "Cantidad"], tablefmt="simple_grid"))
            else:
                print(f"{Fore.RED}{Style.BRIGHT}No existe ningún producto con la marca ingresada.")
        
        elif opcion == '4':
            cursor.execute("SELECT id, nombre, marca, cantidad FROM productos")
            productos = cursor.fetchall()
            if productos:
                print(Fore.WHITE + Style.NORMAL + tabulate(productos, headers=["ID", "Nombre", "Marca", "Cantidad"], tablefmt="simple_grid"))
            else:
                print(f"{Fore.RED}{Style.BRIGHT}No hay productos en el inventario.")
        
        elif opcion == '0':
            print(f"{Fore.BLUE}Volviendo al menú principal...")
            break
        
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Opción no válida. Seleccioná un número entre 0 y 4.")

# Función para ver todos los productos registrados en la base de datos.
def ver_productos(conn, cursor):
    """
    Muestra todos los productos registrados en la base de datos.
    Si no hay productos, le pregunta al usuario si quiere agregar alguno.
    """
    cursor.execute("SELECT id, nombre, marca, cantidad FROM productos")
    productos = cursor.fetchall()
    
    if not productos:
        print(f"{Fore.RED}{Style.BRIGHT}No hay productos registrados en el inventario.\n")
        # Pregunta al usuario si desea agregar un producto
        opcion = input(f"{Fore.WHITE}{Style.BRIGHT}¿Querés agregar un producto?\nIngresá 's' para agregar un producto o presioná 'Enter' para volver al menú principal: ").strip().lower()
        # Elimina espacios adicionales y verifica si la respuesta es "s"
        if opcion == "s":
            agregar_producto(conn, cursor)
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
    else:
        print(f"{Fore.WHITE}{Style.BRIGHT}\nProductos registrados en el inventario:")
        headers = ["ID", "Nombre", "Marca", "Cantidad"]
        print(tabulate(productos, headers=headers, tablefmt="simple_grid"))

# Función para ver los productos con bajo stock
def ver_stock_bajo(conn, cursor):
    """
    Muestra todos los productos con Cantidad <= 2.
    Si no hay productos en la base de datos, le pregunta al usuario si quiere agregar alguno.
    Si hay stock suficiente, se lo indica al usuario.
    """
    # Consulta para verificar si hay productos en la base de datos
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    
    if total_productos == 0:
        print(f"{Fore.RED}{Style.BRIGHT}No hay productos registrados en el inventario.\n")
        # Pregunta al usuario si desea agregar un producto
        opcion = input(f"{Fore.WHITE}{Style.BRIGHT}¿Querés agregar un producto?\nIngresá 's' para agregar un producto o presioná 'Enter' para volver al menú principal: ").strip().lower()
        if opcion == "s":
            agregar_producto(conn, cursor)  # Llama a la función para agregar productos
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
    else:
        # Consulta para obtener productos con cantidad <= 2
        cursor.execute("SELECT id, nombre, marca, cantidad FROM productos WHERE cantidad <= 2")
        productos_bajo_stock = cursor.fetchall()
        
        if not productos_bajo_stock:
            print(f"{Fore.BLUE}{Style.BRIGHT}Hay stock suficiente de todos los productos.Volviendo al menú principal...")
        else:
            # Mostrar resultados con tabulate
            headers = ["ID", "Nombre", "Marca", "Cantidad"]
            print(f"{Fore.WHITE}{Style.BRIGHT}\nProductos con {Fore.RED}stock bajo{Fore.WHITE}:")
            print(tabulate(productos_bajo_stock, headers=headers, tablefmt="simple_grid"))

# Función para eliminar un producto de la base de datos
def eliminar_producto(conn, cursor):
    """
    Sirve para eliminar productos de la base de datos.
    Si no hay productos, se lo indica al usuario y le consulta si quiere agregar algún producto.
    Si hay al menos un producto, le pregunta al usuario si quiere buscar el producto a eliminar por ID, nombre o marca. También le da la opción de volver al menú principal.
    Si no hay productos con el input ingresado, se lo indica al usuario.
    """
    # Consulta para verificar si hay productos en la base de datos
    cursor.execute("SELECT COUNT(*) FROM productos")
    total_productos = cursor.fetchone()[0]
    
    if total_productos == 0:
        print(f"{Fore.RED}{Style.BRIGHT}No hay productos registrados en el inventario.\n")
        # Pregunta al usuario si desea agregar un producto
        opcion = input(f"{Fore.WHITE}{Style.BRIGHT}¿Querés agregar un producto?\n"
            f"Ingresá 's' para agregar un producto o presioná 'Enter' para volver al menú principal: ").strip().lower()
        if opcion == "s":
            agregar_producto(conn, cursor)  # Llama a la función para agregar productos
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
        return  # Termina la función si no hay productos
    else:
        while True:
            # Solicitar al usuario el criterio de búsqueda
            print(f"{Fore.WHITE}{Style.BRIGHT}\n¿Querés buscar el producto a eliminar por...?")
            print("1. ID")
            print("2. Nombre")
            print("3. Marca")
            print("0. Volver al menú principal")
            criterio = input(f"{Fore.WHITE}{Style.BRIGHT}\nSeleccioná una opción: {Fore.YELLOW}")
            
            if criterio == "0":
                print(f"{Fore.BLUE}{Style.BRIGHT}Volviendo al menú principal...")
                return  # Regresa al menú principal
            
            if criterio not in ["1", "2", "3"]:
                print(f"{Fore.RED}{Style.BRIGHT}Opción no válida. Por favor, seleccioná un número entre 0 y 3.")
                continue
            
            productos = []  # Inicializamos la lista productos para evitar el UnboundLocalError

            if criterio == "1":
                busqueda = input(f"{Fore.WHITE}{Style.NORMAL}Si presionás {Style.BRIGHT}'Enter' {Style.NORMAL}verás todos los productos registrados.\n"
                    f"{Fore.WHITE}{Style.BRIGHT}Ingresá el ID del producto a eliminar: {Fore.YELLOW}").strip()
                if not busqueda:  # Si se presiona Enter sin ingresar nada
                    # Mostrar todos los productos registrados
                    cursor.execute("SELECT * FROM productos")
                    productos = cursor.fetchall()
                else:
                    try:
                        busqueda = int(busqueda)
                        # Buscar por ID
                        cursor.execute("SELECT * FROM productos WHERE id = ?", (busqueda,))
                        productos = cursor.fetchall()
                    except ValueError:
                        print(f"{Fore.RED}El ID debe ser un número entero.")
                        continue
            
            elif criterio == "2":
                busqueda = input(f"{Fore.WHITE}{Style.NORMAL}Si presionás {Style.BRIGHT}'Enter' {Style.NORMAL}verás todos los productos registrados.\n"
                    f"{Fore.WHITE}{Style.BRIGHT}Ingresá el nombre del producto a eliminar: {Fore.YELLOW}").strip().lower()
                if busqueda == "0":
                    continue
                # Buscar por nombre
                cursor.execute("SELECT * FROM productos WHERE LOWER(nombre) LIKE ?", ('%' + busqueda + '%',))
                productos = cursor.fetchall()
            
            elif criterio == "3":
                busqueda = input(f"{Fore.WHITE}{Style.NORMAL}Si presionás {Style.BRIGHT}'Enter' {Style.NORMAL}verás todos los productos registrados.\n"
                    f"{Fore.WHITE}{Style.BRIGHT}Ingresá la marca del producto a eliminar: {Fore.YELLOW}").strip().lower()
                if busqueda == "0":
                    continue
                # Buscar por marca
                cursor.execute("SELECT * FROM productos WHERE LOWER(marca) LIKE ?", ('%' + busqueda + '%',))
                productos = cursor.fetchall()
            
            if productos:
                # Mostrar resultados encontrados con tabulate en formato simple_grid
                headers = ["ID", "Nombre", "Marca", "Cantidad"]
                print(f"{Fore.WHITE}\nProductos encontrados:")
                print(tabulate(productos, headers=headers, tablefmt="simple_grid"))
                
                # Pedir ID para eliminar
                id_producto = input(f"{Fore.WHITE}Presioná {Style.BRIGHT}'Enter' {Style.NORMAL}para cancelar.\n"
                    f"{Style.BRIGHT}Ingresá el ID del producto a eliminar: {Fore.YELLOW}").strip()
                
                if not id_producto.isdigit() or int(id_producto) == 0:
                    print(f"{Fore.BLUE}{Style.BRIGHT}Operación cancelada.")
                    continue
                
                cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
                producto = cursor.fetchone()
                
                if producto:
                    # Confirmación de eliminación
                    print(f"{Fore.WHITE}{Style.BRIGHT}\n¿Querés confirmar la eliminación del siguiente producto?")
                    print(tabulate([producto], headers=headers, tablefmt="simple_grid"))
                    
                    confirmacion = input(f"{Fore.WHITE}Presioná {Style.BRIGHT}'Enter' {Style.NORMAL}para cancelar\n"
                        f"{Style.BRIGHT}Ingresá 's' para confirmar: ").strip().lower()
                    
                    if confirmacion == 's':
                        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                        conn.commit()
                        print(f"{Fore.GREEN}{Style.BRIGHT}Producto con ID {id_producto} eliminado exitosamente.")
                    else:
                        print(f"{Fore.BLUE}{Style.BRIGHT}Eliminación cancelada.")
                else:
                    print(f"{Fore.RED}{Style.BRIGHT}No se encontró el producto con ese ID.")
            else:
                print(f"{Fore.RED}{Style.BRIGHT}No se encontraron productos con esa búsqueda.")
