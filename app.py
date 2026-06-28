from flask import Flask, render_template, request, redirect, flash, session, url_for
from datetime import datetime
import mysql.connector
import hashlib
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key'


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="college_db"
)
cursor = db.cursor()

@app.context_processor
def inject_now():
    return {'now': datetime.now}



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            session['username'] = username
            session['role'] = user[3]
            flash("✅ Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("❌ Invalid username or password.", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("🚪 Logged out successfully!", "info")
    return redirect(url_for('login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("⚠️ Please login to continue.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def home():
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS total_students FROM students")
    total_students = cur.fetchone()['total_students']

    cur.execute("SELECT COUNT(*) AS total_courses FROM courses")
    total_courses = cur.fetchone()['total_courses']

    cur.execute("SELECT COUNT(*) AS total_faculty FROM faculty")
    total_faculty = cur.fetchone()['total_faculty']

    cur.execute("SELECT COUNT(*) AS total_enrollments FROM enrollments")
    total_enrollments = cur.fetchone()['total_enrollments']

    cur.execute("SELECT COUNT(*) AS total_departments FROM departments")
    total_departments = cur.fetchone()['total_departments']

    cur.execute("""
        SELECT d.dept_name, d.hod, COUNT(s.student_id) AS student_count
        FROM departments d
        LEFT JOIN students s ON d.dept_id = s.dept_id
        GROUP BY d.dept_id, d.dept_name, d.hod
    """)
    departments = cur.fetchall()

    department_labels = [dept.get('dept_name') or 'Unknown' for dept in departments]
    department_counts = [dept.get('student_count', 0) for dept in departments]

    return render_template('index.html',
                           total_students=total_students,
                           total_courses=total_courses,
                           total_faculty=total_faculty,
                           total_enrollments=total_enrollments,
                           total_departments=total_departments,
                           departments=departments,
                           department_labels=department_labels,
                           department_counts=department_counts)



@app.route('/departments')
@login_required
def view_departments():
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM departments ORDER BY dept_id ASC")
    departments = cur.fetchall()
    return render_template('view_departments.html', departments=departments)

@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    if request.method == 'POST':
        dept_name = request.form['dept_name']
        hod = request.form['hod']
        location = request.form['location']

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO departments (dept_name, hod, location) VALUES (%s, %s, %s)",
            (dept_name, hod, location)
        )
        mysql.connection.commit()
        cursor.close()

        flash('Department added successfully!', 'success')
        return redirect(url_for('view_departments'))
    
    return render_template('add_department.html')


@app.route('/delete_department/<int:id>')
@login_required
def delete_department(id):
    cursor.execute("DELETE FROM departments WHERE dept_id = %s", (id,))
    db.commit()
    flash("🗑️ Department deleted successfully!", "success")
    return redirect('/departments')

@app.route('/students')
@login_required
def view_students():
    department_filter = request.args.get('department')
    cur = db.cursor(dictionary=True)

    query = """
        SELECT s.*, d.dept_name 
        FROM students s 
        LEFT JOIN departments d ON s.dept_id = d.dept_id
    """
    params = []

    if department_filter:
        query += " WHERE d.dept_name = %s"
        params.append(department_filter)

    query += " ORDER BY s.student_id ASC"

    cur.execute(query, tuple(params))
    students = cur.fetchall()
    return render_template('view_students.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        dept_id = request.form['dept_id']
        email = request.form['email']

        cursor.execute("""
            INSERT INTO students (name, age, gender, dept_id, email)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, age, gender, dept_id, email))
        db.commit()
        flash("✅ Student added successfully!", "success")
        return redirect('/students')
    return render_template('add_student.html', departments=departments)


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE student_id = %s", (id,))
    student = cur.fetchone()
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()

    if not student:
        flash("❌ Student not found.", "danger")
        return redirect('/students')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        dept_id = request.form['dept_id']
        email = request.form['email']

        cur.execute("""
            UPDATE students SET name=%s, age=%s, gender=%s, dept_id=%s, email=%s
            WHERE student_id=%s
        """, (name, age, gender, dept_id, email, id))
        db.commit()
        flash("✏️ Student updated successfully!", "success")
        return redirect('/students')

    return render_template('edit_student.html', student=student, departments=departments)


@app.route('/delete_student/<int:id>')
@login_required
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE student_id = %s", (id,))
    db.commit()
    flash("🗑️ Student deleted successfully!", "success")
    return redirect('/students')




@app.route('/faculty')
def view_faculty():
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT f.*, d.dept_name 
        FROM faculty f
        LEFT JOIN departments d ON f.dept_id = d.dept_id
        ORDER BY f.faculty_id ASC
    """)
    faculty = cur.fetchall()
    return render_template('view_faculty.html', faculty=faculty)


@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        dept_id = request.form['dept_id']
        email = request.form['email']
        salary = request.form['salary']

        cursor.execute("""
            INSERT INTO faculty (name, designation, dept_id, email, salary)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, designation, dept_id, email, salary))
        db.commit()
        flash("✅ Faculty added successfully!", "success")
        return redirect('/faculty')
    return render_template('add_faculty.html', departments=departments)


@app.route('/edit_faculty/<int:id>', methods=['GET', 'POST'])
def edit_faculty(id):
    cur = db.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        dept_id = request.form['dept_id']
        email = request.form['email']
        salary = request.form['salary']

        cur.execute("""
            UPDATE faculty 
            SET name=%s, designation=%s, dept_id=%s, email=%s, salary=%s
            WHERE faculty_id=%s
        """, (name, designation, dept_id, email, salary, id))
        db.commit()
        flash("✏️ Faculty updated successfully!", "success")
        return redirect('/faculty')

    cur.execute("SELECT * FROM faculty WHERE faculty_id = %s", (id,))
    faculty = cur.fetchone()
    cur.execute("SELECT * FROM departments")
    departments = cur.fetchall()
    return render_template('edit_faculty.html', faculty=faculty, departments=departments)


@app.route('/delete_faculty/<int:id>')
def delete_faculty(id):
    cursor.execute("DELETE FROM faculty WHERE faculty_id = %s", (id,))
    db.commit()
    flash("🗑️ Faculty deleted successfully!", "success")
    return redirect('/faculty')




@app.route('/enrollments')
def view_enrollments():
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT e.enrollment_id, s.name AS student_name, c.course_name, e.semester, e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        ORDER BY e.enrollment_id ASC
    """)
    enrollments = cur.fetchall()
    return render_template('view_enrollments.html', enrollments=enrollments)


@app.route('/add_enrollment', methods=['GET', 'POST'])
def add_enrollment():
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT s.student_id, s.name, d.dept_name FROM students s JOIN departments d ON s.dept_id = d.dept_id ORDER BY s.name")
    students = cur.fetchall()
    cur.execute("SELECT * FROM courses")
    courses = cur.fetchall()

    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        semester = request.form.get('semester')
        grade = request.form.get('grade')

        cursor.execute("""
            INSERT INTO enrollments (student_id, course_id, semester, grade)
            VALUES (%s, %s, %s, %s)
        """, (student_id, course_id, semester, grade))
        db.commit()
        flash("✅ Enrollment added successfully!", "success")
        return redirect('/enrollments')
    return render_template('add_enrollment.html', students=students, courses=courses)


@app.route('/delete_enrollment/<int:id>')
def delete_enrollment(id):
    cursor.execute("DELETE FROM enrollments WHERE enrollment_id = %s", (id,))
    db.commit()
    flash("🗑️ Enrollment deleted successfully!", "success")
    return redirect('/enrollments')



if __name__ == '__main__':
    app.run(debug=True)
