import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# Get existing prof_id or default to 1
prof_id = 1

# List of all 6 Theory and 4 Lab sessions from the official timetable (GLBAJAJ, CSE-AIML&CS, Sec H, Sem III)
schedules_data = [
    # Theory Courses (Room 242, Block-B)
    {
        "id": 1,
        "course_name": "PYTHON",
        "full_name": "Python Programming (BCC302)",
        "course_type": "theory",
        "room_or_lab": "Room 242 (Block-B)",
        "faculty_name": "Er. Bhanu Pratap Singh",
        "target_group": "All",
        "time_slot": "Mon 09:10-10:00, Wed 09:10-10:00, Thu 12:41-01:30, Fri 11:01-11:50",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 2,
        "course_name": "MATH-IV",
        "full_name": "Math IV (BAS303)",
        "course_type": "theory",
        "room_or_lab": "Room 242 (Block-B)",
        "faculty_name": "Dr. Ashish Kumar",
        "target_group": "All",
        "time_slot": "Mon 10:01-10:50, Tue 09:10-10:00, Wed 12:41-01:30, Thu 09:10-10:00, Fri 11:51-12:40",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 3,
        "course_name": "DS",
        "full_name": "Data Structure (BCS301)",
        "course_type": "theory",
        "room_or_lab": "Room 242 (Block-B)",
        "faculty_name": "Er. Richa Mishra",
        "target_group": "All",
        "time_slot": "Mon 11:01-11:50, Tue 10:01-10:50, Wed 10:01-10:50, Thu 11:01-11:50, Fri 12:41-01:30",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 4,
        "course_name": "DSTL",
        "full_name": "Discrete Structures & Theory of Logic (BCS303)",
        "course_type": "theory",
        "room_or_lab": "Room 242 (Block-B)",
        "faculty_name": "Er. Gopal Singh",
        "target_group": "All",
        "time_slot": "Mon 11:51-12:40, Wed 11:51-12:40, Thu 11:51-12:40, Fri 09:10-10:00",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 5,
        "course_name": "COA",
        "full_name": "Computer Organization & Architecture (BCS302)",
        "course_type": "theory",
        "room_or_lab": "Room 242 (Block-B)",
        "faculty_name": "Er. Hitendra Kumar Prajapati",
        "target_group": "All",
        "time_slot": "Tue 02:21-04:00, Wed 11:01-11:50, Thu 10:01-10:50, Fri 10:01-10:50",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 6,
        "course_name": "UHV",
        "full_name": "Universal Human Values (BVE301)",
        "course_type": "theory",
        "room_or_lab": "Room 242 (Block-B)",
        "faculty_name": "Dr. Bablu Kumar Jha",
        "target_group": "All",
        "time_slot": "Tue 04:01-04:50, Wed 02:21-03:10, Fri 04:01-04:50",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },

    # --- 4 LAB SESSIONS ---
    {
        "id": 7,
        "course_name": "Web Designing Workshop",
        "full_name": "Web Designing Workshop (BCS353)",
        "course_type": "lab",
        "room_or_lab": "Lab-11 (Room 321) / Lab-04",
        "faculty_name": "Er. Gopal Singh",
        "target_group": "G1: Tue 11:01-12:40 (Lab-11) | G2: Thu 02:21-04:00 (Lab-04)",
        "time_slot": "Tue 11:01-12:40 (G1) / Thu 02:21-04:00 (G2)",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 8,
        "course_name": "Data Structure Lab",
        "full_name": "Data Structure Lab (BCS351)",
        "course_type": "lab",
        "room_or_lab": "Lab-05",
        "faculty_name": "Er. Richa Mishra",
        "target_group": "G1: Wed 03:11-04:50 (Lab-05) | G2: Fri 02:21-04:00 (Lab-05)",
        "time_slot": "Wed 03:11-04:50 (G1) / Fri 02:21-04:00 (G2)",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 9,
        "course_name": "COA Lab",
        "full_name": "Computer Organization & Architecture Lab (BCS352)",
        "course_type": "lab",
        "room_or_lab": "Lab-07 / Lab-03",
        "faculty_name": "Er. Hitendra Kumar Prajapati",
        "target_group": "G2: Tue 11:01-12:40 (Lab-07) | G1: Thu 02:21-04:00 (Lab-03)",
        "time_slot": "Tue 11:01-12:40 (G2) / Thu 02:21-04:00 (G1)",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    },
    {
        "id": 10,
        "course_name": "Mini Project Lab",
        "full_name": "Internship Assessment / Mini Project (BCC351)",
        "course_type": "lab",
        "room_or_lab": "Lab-06",
        "faculty_name": "Er. Gopal Singh / Er. Hitendra Kumar Prajapati",
        "target_group": "G2: Wed 03:11-04:50 (Lab-06) | G1: Fri 02:21-04:00 (Lab-06)",
        "time_slot": "Wed 03:11-04:50 (G2) / Fri 02:21-04:00 (G1)",
        "lat": 27.646560,
        "lng": 77.551925,
        "allowed_radius_m": 100.0
    }
]

for s in schedules_data:
    existing = cursor.execute("SELECT id FROM schedules WHERE id=?", (s["id"],)).fetchone()
    if existing:
        cursor.execute("""
            UPDATE schedules 
            SET course_name=?, full_name=?, course_type=?, room_or_lab=?, faculty_name=?, target_group=?, time_slot=?, lat=?, lng=?, allowed_radius_m=?
            WHERE id=?
        """, (s["course_name"], s["full_name"], s["course_type"], s["room_or_lab"], s["faculty_name"], s["target_group"], s["time_slot"], s["lat"], s["lng"], s["allowed_radius_m"], s["id"]))
    else:
        cursor.execute("""
            INSERT INTO schedules (id, course_name, prof_id, lat, lng, allowed_radius_m, full_name, course_type, room_or_lab, faculty_name, target_group, time_slot)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (s["id"], s["course_name"], prof_id, s["lat"], s["lng"], s["allowed_radius_m"], s["full_name"], s["course_type"], s["room_or_lab"], s["faculty_name"], s["target_group"], s["time_slot"]))

conn.commit()
print("Schedules successfully seeded/updated!")
all_s = cursor.execute("SELECT id, course_name, course_type, room_or_lab, faculty_name FROM schedules").fetchall()
for row in all_s:
    print(f"[{row[0]}] {row[1]} ({row[2]}) - {row[3]} - {row[4]}")
conn.close()
