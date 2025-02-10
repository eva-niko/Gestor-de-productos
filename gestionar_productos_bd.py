from colorama import Fore, Style
import unicodedata

def normalizar_texto_bd(texto):
    """
    Convierte texto con tildes a texto sin tildes, conserva la letra ñ,
    y transforma el texto a minúsculas.
    """
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Reconstruir la 'ñ' de 'n' + diacrítico, si está descompuesta
    texto_normalizado = texto_normalizado.replace('ñ', 'ñ').replace('Ñ', 'Ñ')
    # Eliminar los diacríticos (acentos) de los demás caracteres
    texto_sin_tildes = ''.join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )
    return texto_sin_tildes.lower()  # Convertir a minúsculas

def gestionar_producto(conn, cursor, id_producto=None, nombre=None, marca=None, cantidad=None, operacion="insertar"):
    """
    Gestiona operaciones CRUD normalizadas en la tabla de productos.
    
    :param conn: Conexión a la base de datos.
    :param cursor: Cursor de la base de datos.
    :param id_producto: ID del producto (para operaciones de actualización).
    :param nombre: Nombre del producto (normalizado automáticamente).
    :param marca: Marca del producto (normalizado automáticamente).
    :param cantidad: Cantidad del producto.
    :param operacion: Tipo de operación: 'insertar', 'actualizar' o 'agregar_cantidad'.
    """
    # Normalizar texto si se proporciona
    if nombre:
        nombre = normalizar_texto_bd(nombre)
    if marca:
        marca = normalizar_texto_bd(marca)
    
    if operacion == "insertar":
        # Insertar nuevo producto
        cursor.execute("INSERT INTO productos (nombre, marca, cantidad) VALUES (?, ?, ?)", (nombre, marca, cantidad))
        print(Fore.GREEN + Style.BRIGHT + f"Producto: '{nombre}' - Marca: '{marca}' añadido. Cantidad: {cantidad}\n")
        return nombre  # Devolver el nombre insertado

    elif operacion == "actualizar" and id_producto:
        # Actualizar campos específicos de un producto existente
        if nombre:
            cursor.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nombre, id_producto))
        if marca:
            cursor.execute("UPDATE productos SET marca = ? WHERE id = ?", (marca, id_producto))
        if cantidad is not None:
            cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (cantidad, id_producto))
        print(Fore.GREEN + Style.BRIGHT + f"\nProducto con ID {id_producto} actualizado.")
        
        # Ahora, obtén la nueva marca desde la base de datos para devolverla
        cursor.execute("SELECT marca FROM productos WHERE id = ?", (id_producto,))
        producto_actualizado = cursor.fetchone()
        return producto_actualizado[0] if producto_actualizado else None  # Devolver la marca actualizada

    elif operacion == "agregar_cantidad" and nombre and marca:
        # Verificar si el producto ya existe
        cursor.execute("SELECT cantidad FROM productos WHERE nombre = ? AND marca = ?", (nombre, marca))
        producto = cursor.fetchone()
        if producto:
            # Si existe, actualizar cantidad
            nueva_cantidad = producto[0] + cantidad
            cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ? AND marca = ?", (nueva_cantidad, nombre, marca))
            print(Fore.GREEN + Style.BRIGHT + f"\nCantidad del Producto: '{nombre}' - Marca: '{marca}' actualizada.\nNueva cantidad: {nueva_cantidad}\n")
        else:
            # Si no existe, insertar nuevo producto
            cursor.execute("INSERT INTO productos (nombre, marca, cantidad) VALUES (?, ?, ?)", (nombre, marca, cantidad))
            print(Fore.GREEN + Style.BRIGHT + f"Producto: '{nombre}' - Marca: '{marca}' añadido. Cantidad: {cantidad}\n")
        return nombre  # Devolver el nombre después de la operación

    else:
        print(Fore.RED + "Operación no válida.")
        return None  # Si la operación no es válida, retornar None
    
    conn.commit()