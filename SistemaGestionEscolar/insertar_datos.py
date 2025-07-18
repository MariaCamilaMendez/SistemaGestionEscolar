import mysql.connector

# Establecer la conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",  # Cambia esto si tu servidor MySQL está en otro lugar
    user="lol",  
    password="",  # 
    database="SistemaGestionEscolar"  # Nombre de la base de datos
)

cursor = conn.cursor()

# Insertar datos en la tabla Teachers
try:
    cursor.execute("""
        INSERT INTO Teachers (first_name, last_name, email, hire_date)
        VALUES 
        ('Ana', 'Torres', 'ana.torres@example.com', '2020-02-01'),
        ('Alvaro', 'Hurtado', 'alvaro.hurtado@example.com', '2019-05-15');
    """)
    print("Datos de profesores insertados correctamente.")
except mysql.connector.Error as err:
    print(f"Error al insertar datos en Teachers: {err}")


# Insertar datos en la tabla Courses
try:
    cursor.execute("""
        INSERT INTO Courses (course_name, teacher_id)
        VALUES 
        ('Matemáticas', 1),  # Ana Torres
        ('Historia', 2);     # Luis Martínez
    """)
    print("Datos de cursos insertados correctamente.")
except mysql.connector.Error as err:
    print(f"Error al insertar datos en Courses: {err}")



# Insertar datos en la tabla Students
try:
    cursor.execute("""
        INSERT INTO Students (first_name, last_name, email, date_of_birth)
        VALUES 
        ('Maria', 'Mendez', 'maria.mendez@example.com', '2000-01-15'),
        ('María', 'Gómez', 'maria.gomez@example.com', '1999-03-22'),
        ('Juan', 'Perez', 'juan.perez@example.com', '2001-07-10');
    """)
    print("Datos de estudiantes insertados correctamente.")
except mysql.connector.Error as err:
    print(f"Error al insertar datos en Students: {err}")



try:
    cursor.execute("""
        INSERT INTO Enrollments (student_id, course_id)
        VALUES 
        (20, 1),  # Juan Pérez se matricula en Matemáticas
        (21, 1),  # María Gómez se matricula en Matemáticas
        (22, 2);  # Juan Pérez se matricula en Historia
    """)
    print("Datos de matrículas insertados correctamente.")
except mysql.connector.Error as err:
    print(f"Error al insertar datos en Enrollments: {err}")


conn.commit()


cursor.close()
conn.close()





 