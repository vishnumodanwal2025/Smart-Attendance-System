import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# 1. Update users table
cols = [c[1] for c in cursor.execute('PRAGMA table_info(users)').fetchall()]
for col in ['enrollment_no', 'section', 'group']:
    if col not in cols:
        cursor.execute(f'ALTER TABLE users ADD COLUMN "{col}" TEXT')
        print(f"Added column '{col}' to users table")

# 2. Update schedules table to support lab type, timings, room, group
s_cols = [c[1] for c in cursor.execute('PRAGMA table_info(schedules)').fetchall()]
for col in ['full_name', 'course_type', 'room_or_lab', 'faculty_name', 'target_group', 'time_slot']:
    if col not in s_cols:
        cursor.execute(f'ALTER TABLE schedules ADD COLUMN "{col}" TEXT')
        print(f"Added column '{col}' to schedules table")

conn.commit()
print("Migration completed successfully!")
print("Users columns:", [c[1] for c in cursor.execute('PRAGMA table_info(users)').fetchall()])
print("Schedules columns:", [c[1] for c in cursor.execute('PRAGMA table_info(schedules)').fetchall()])
conn.close()
