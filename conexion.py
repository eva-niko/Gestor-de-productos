import sqlite3
from colorama import Fore, Style, init

# Inicializar colorama para que funcione correctamente en Windows
init(autoreset=True)

def conectar_bd():
    conn = sqlite3.connect('inventario.db')  # Conexión a la base de datos
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "productos" (
            "id" INTEGER,
            "nombre" TEXT NOT NULL,
            "marca" TEXT NOT NULL,
            "cantidad" INTEGER NOT NULL,
            PRIMARY KEY("id")
        );
    ''')  # Crear tabla si no existe
    conn.commit()
    return conn, cursor
