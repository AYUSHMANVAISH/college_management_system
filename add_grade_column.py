import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="college_db"
)
cursor = db.cursor()

try:
    cursor.execute("ALTER TABLE enrollments ADD COLUMN grade VARCHAR(10) DEFAULT NULL;")
    db.commit()
    print("Grade column added successfully.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    db.close()
