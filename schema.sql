-- Use or create the database
CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- Drop existing tables to avoid conflicts
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

-- Create the students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INT,
    gender VARCHAR(20),
    department VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(15),
    address VARCHAR(255)
);

-- Create the courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    credits INT
);

-- Create the enrollments table (with cascading foreign keys)
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Insert sample students
INSERT INTO students (name, age, gender, department, email, phone, address) VALUES
('Ayushman', 21, 'Male', 'Computer Science', 'ayushman@example.com', '9876543210', 'Delhi'),
('Riya', 22, 'Female', 'Electronics', 'riya@example.com', '9876500000', 'Mumbai'),
('Karan', 20, 'Male', 'Mechanical', 'karan@example.com', '9876511111', 'Bangalore'),
('Sneha', 23, 'Female', 'Civil', 'sneha@example.com', '9876522222', 'Pune'),
('Arjun', 21, 'Male', 'Electrical', 'arjun@example.com', '9876533333', 'Kolkata');

-- Insert sample courses
INSERT INTO courses (course_name, credits) VALUES
('Database Systems', 3),
('Operating Systems', 4),
('Computer Networks', 3),
('Data Structures', 3),
('Software Engineering', 3);

-- Insert sample enrollments
INSERT INTO enrollments (student_id, course_id, grade) VALUES
(1, 1, 'A'),
(1, 2, 'B'),
(2, 3, 'A'),
(3, 4, 'C'),
(4, 5, 'B'),
(5, 1, 'A');