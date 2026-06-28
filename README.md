# College Management System

A Python Flask-based web application integrated with a MySQL database to manage student, faculty, department, and course enrollment records.

## Features

- **User Authentication**: Secure login and logout system for admin/staff.
- **Student Management**: View, add, update, and delete student profiles.
- **Faculty Management**: View, add, edit, and remove faculty member profiles (designation, department, salary, email).
- **Department Management**: Monitor and add departments, track HODs, and student distributions.
- **Enrollment Tracking**: Enroll students in courses and assign/view grades.
- **Interactive Dashboard**: Rich statistics displaying overall counts (students, faculty, departments, enrollments) and a visual department-wise student breakdown.

## Project Structure

- `app.py`: Main Flask application entrypoint containing routes and database configurations.
- `schema.sql`: Complete MySQL schema initialization script with sample seed data.
- `migrations/`: Folder containing database schema migrations.
- `templates/`: HTML templates rendered via Jinja2 engine (styled with Bootstrap and FontAwesome).
- `static/`: CSS styling sheets.

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS (Bootstrap 5 + Custom Styling), FontAwesome Icons, Chart.js

## Installation & Setup

### Prerequisites

- Python 3.x
- MySQL Server

### 1. Database Setup

1. Open your MySQL client and run the SQL script `schema.sql` to create the database (`college_db`) and populate tables with sample data:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Apply migrations (if any):
   ```bash
   mysql -u root -p college_db < migrations/001_convert_gender_to_enum.sql
   ```

### 2. Application Setup

1. Install Python dependencies:
   ```bash
   pip install flask mysql-connector-python
   ```
2. Update database connection settings in `app.py` if your MySQL username, password, or host differ:
   ```python
   db = mysql.connector.connect(
       host="localhost",
       user="root",
       password="your-password",
       database="college_db"
   )
   ```

### 3. Running the Server

Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000/`.
