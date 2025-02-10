from conexion import conectar_bd
from funciones_menu import (
    eliminar_producto, modificar_producto_bd,
    agregar_producto, buscar_producto, ver_productos,
    ver_stock_bajo
)
from colorama import Fore, Style

def mostrar_menu():
    print(f"{Fore.WHITE}{Style.BRIGHT}\nMenú de productos")
    menu_text = [
        "1. Añadir producto",
        "2. Modificar producto",
        "3. Buscar producto",
        "4. Ver productos",
        "5. Ver productos con stock bajo",
        "6. Eliminar producto",
        "0. Salir"
    ]
    for item in menu_text:
        print(Fore.WHITE + item)

def main():
    conn, cursor = conectar_bd()

    while True:
        mostrar_menu()
        opcion = input(f"{Fore.WHITE}{Style.BRIGHT}\nSeleccioná una opción: {Fore.YELLOW}{Style.BRIGHT}").strip()

        if opcion == '1':
            agregar_producto(conn, cursor)
        elif opcion == '2':
            modificar_producto_bd(conn, cursor)
        elif opcion == '3':
            buscar_producto(conn, cursor)
        elif opcion == '4':
            ver_productos(conn, cursor)
        elif opcion == '5':
            ver_stock_bajo(conn, cursor)
        elif opcion == '6':
            eliminar_producto(conn, cursor)
        elif opcion == '0':
            print(f"{Fore.BLUE}{Style.BRIGHT}Saliendo del programa...\n")
            break
        else:
            print(f"{Fore.RED}Opción no válida. Seleccioná un número entre 0 y 6.")

    conn.close()

if __name__ == "__main__":
    main()