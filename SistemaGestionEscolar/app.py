from flask import Flask, render_template, request, redirect, url_for, flash
from conexion import get_connection  

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estudiantes')
def listar_estudiantes():
    print("Entre Aqui")
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('estudiantes.html', estudiantes=estudiantes)

@app.route('/profesores')
def listar_profesores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM teachers")
    profesores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('profesores.html', profesores=profesores)

@app.route('/cursos')
def listar_cursos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('cursos.html', cursos=cursos)

@app.route('/matriculacion', methods=['GET', 'POST'])
def matriculacion():

    connection = get_connection()
    cursorCursos = connection.cursor(dictionary=True)
    cursor = connection.cursor(dictionary=True)

    cursorEstudiantes = connection.cursor(dictionary=True)


    if request.method == 'GET':
    
        cursorCursos.execute('SELECT * FROM Courses')
        cursos = cursorCursos.fetchall()
        
        
        cursorEstudiantes.execute('SELECT * FROM Students')
        estudiantes = cursorEstudiantes.fetchall()
        
        return render_template('matriculacion.html', cursos=cursos, estudiantes=estudiantes)

    if request.method == 'POST':
        student_id = request.form['student_id']
        course_ids = request.form.getlist('course_ids')  
        
        
        cursorEstudiantes.execute('SELECT * FROM Students WHERE id = %s', (student_id,))
        student = cursorEstudiantes.fetchone()
        
        if student:
            for course_id in course_ids:
                cursor.execute(
                    'INSERT INTO Enrollments (student_id, course_id) VALUES (%s, %s)',
                    (student_id, course_id)
                )
            connection.commit()
            flash('¡Te has matriculado con éxito!', 'success')
        else:
            flash('Estudiante no encontrado', 'danger')
        
        return redirect(url_for('matriculacion'))

    connection.close()

@app.route('/reportes')
def mostrar_reportes():
    conn = get_connection()

    cursorCount = conn.cursor(dictionary=True)
    cursorCount.execute("""
        SELECT Courses.course_name, COUNT(Enrollments.student_id) AS total_estudiantes
        FROM Courses
        LEFT JOIN Enrollments ON Courses.id = Enrollments.course_id
        GROUP BY Courses.course_name
    """)
    reportes = cursorCount.fetchall()
    cursorCount.close()

    cursorEstudiantes = conn.cursor(dictionary=True)
    cursorEstudiantes.execute("""
        select s.first_name, s.last_name, c.course_name, t.first_name as prof from students s
        right join enrollments e on e.student_id = s.id
        join courses c on c.id = e.course_id
        join teachers t on t.id = c.teacher_id  
        and t.id = (select id from teachers t1 
                    where t1.first_name = "Ana" and t1.last_name = "Torres")
    """)
    estudiantes = cursorEstudiantes.fetchall()
    cursorEstudiantes.close()

    cursorCursos = conn.cursor(dictionary=True)
    cursorCursos.execute("""
        SELECT s.first_name, s.last_name
        FROM Students s
        JOIN Enrollments e ON s.id = e.student_id
        WHERE e.course_id = (SELECT id FROM Courses WHERE course_name = 'Programacion de bases de datos');
    """)
    cursos = cursorCursos.fetchall()
    cursorCursos.close()

    cursorCursosCount = conn.cursor(dictionary=True)
    cursorCursosCount.execute("""
        SELECT Courses.course_name, COUNT(Enrollments.student_id) AS total_estudiantes
        FROM Courses
        LEFT JOIN Enrollments ON Courses.id = Enrollments.course_id
        GROUP BY Courses.course_name
    """)
    curso_estudiantes = cursorCursosCount.fetchall()
    cursorCursosCount.close()

    cursorTeachers = conn.cursor(dictionary=True)
    cursorTeachers.execute("""
        SELECT t.first_name, t.last_name, COUNT(e.student_id) AS total_students
        FROM Teachers t
        JOIN Courses c ON t.id = c.teacher_id
        JOIN Enrollments e ON c.id = e.course_id
        GROUP BY t.id
        ORDER BY total_students DESC;
    """)
    teachers_report = cursorTeachers.fetchall()
    cursorTeachers.close()

    conn.close()

    return render_template('reportes.html', reportes=reportes, estudiantes=estudiantes, cursos=cursos ,curso_estudiantes=curso_estudiantes, teachers_report=teachers_report)

if __name__ == '__main__':
    app.run(debug=True)
