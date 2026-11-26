import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute("UPDATE schedules SET faculty_name = 'Dr. Ashish Kumar' WHERE course_name = 'MATH-IV'")
conn.commit()
print("Updated MATH-IV in DB:", cursor.execute("SELECT id, course_name, faculty_name FROM schedules WHERE course_name = 'MATH-IV'").fetchall())
conn.close()
