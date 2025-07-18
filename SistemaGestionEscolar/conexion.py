import mysql.connector


def get_connection():
    
    conexion = mysql.connector.connect(
        host="localhost",
        user="lol",  
        password="",  
        database="SistemaGestionEscolar" 
    )
    return conexion


conexion = get_connection()
if conexion.is_connected():
    print("Conexión exitosa a la base de datos")

    
    cursor = conexion.cursor()

    
    cursor.execute("SHOW TABLES;")
    tablas = cursor.fetchall()

    print("Tablas en la base de datos:")
    for tabla in tablas:
        print(tabla)

    cursor.close()
else:
    print("Error en la conexión")


conexion.close()
