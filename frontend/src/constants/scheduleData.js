export const API_BASE = "http://127.0.0.1:8000";

export const CAMPUS_COORDINATES = {
  lat: 27.646560,
  lng: 77.551925
};

export const STATIC_SCHEDULE_DATA = [
  {
    id: 1,
    course_name: "PYTHON",
    full_name: "Python Programming (BCC302)",
    course_type: "theory",
    faculty_name: "Er. Bhanu Pratap Singh",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 09:10-10:00, Wed 09:10-10:00, Thu 12:41-01:30, Fri 11:01-11:50",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#003087",
    icon: "🐍"
  },
  {
    id: 2,
    course_name: "MATH-IV",
    full_name: "Math IV (BAS303)",
    course_type: "theory",
    faculty_name: "Dr. Ashish Kumar",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 10:01-10:50, Tue 09:10-10:00, Wed 12:41-01:30, Thu 09:10-10:00, Fri 11:51-12:40",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#C0392B",
    icon: "∫"
  },
  {
    id: 3,
    course_name: "DS",
    full_name: "Data Structure (BCS301)",
    course_type: "theory",
    faculty_name: "Er. Richa Mishra",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 11:01-11:50, Tue 10:01-10:50, Wed 10:01-10:50, Thu 11:01-11:50, Fri 12:41-01:30",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#00897B",
    icon: "🌲"
  },
  {
    id: 4,
    course_name: "DSTL",
    full_name: "Discrete Structures & Theory of Logic (BCS303)",
    course_type: "theory",
    faculty_name: "Er. Gopal Singh",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 11:51-12:40, Wed 11:51-12:40, Thu 11:51-12:40, Fri 09:10-10:00",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#D97706",
    icon: "Σ"
  },
  {
    id: 5,
    course_name: "COA",
    full_name: "Computer Organization & Architecture (BCS302)",
    course_type: "theory",
    faculty_name: "Er. Hitendra Kumar Prajapati",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Tue 02:21-04:00, Wed 11:01-11:50, Thu 10:01-10:50, Fri 10:01-10:50",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#2563EB",
    icon: "💻"
  },
  {
    id: 6,
    course_name: "UHV",
    full_name: "Universal Human Values (BVE301)",
    course_type: "theory",
    faculty_name: "Dr. Bablu Kumar Jha",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Tue 04:01-04:50, Wed 02:21-03:10, Fri 04:01-04:50",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#4B5563",
    icon: "🤝"
  },
  // 4 LAB SESSIONS
  {
    id: 7,
    course_name: "Web Designing Workshop",
    full_name: "Web Designing Workshop Lab (BCS353)",
    course_type: "lab",
    faculty_name: "Er. Gopal Singh",
    room_or_lab: "Lab-11 (Room 321) / Lab-04",
    target_group: "G1: Tue 11:01-12:40 (Lab-11) | G2: Thu 02:21-04:00 (Lab-04)",
    time_slot: "Tue 11:01-12:40 (G1) / Thu 02:21-04:00 (G2)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#6A1B9A",
    icon: "🌐"
  },
  {
    id: 8,
    course_name: "Data Structure Lab",
    full_name: "Data Structure Lab (BCS351)",
    course_type: "lab",
    faculty_name: "Er. Richa Mishra",
    room_or_lab: "Lab-05",
    target_group: "G1: Wed 03:11-04:50 (Lab-05) | G2: Fri 02:21-04:00 (Lab-05)",
    time_slot: "Wed 03:11-04:50 (G1) / Fri 02:21-04:00 (G2)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#00897B",
    icon: "🧪"
  },
  {
    id: 9,
    course_name: "COA Lab",
    full_name: "Computer Organization & Architecture Lab (BCS352)",
    course_type: "lab",
    faculty_name: "Er. Hitendra Kumar Prajapati",
    room_or_lab: "Lab-07 / Lab-03",
    target_group: "G2: Tue 11:01-12:40 (Lab-07) | G1: Thu 02:21-04:00 (Lab-03)",
    time_slot: "Tue 11:01-12:40 (G2) / Thu 02:21-04:00 (G1)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#1565C0",
    icon: "⚙️"
  },
  {
    id: 10,
    course_name: "Mini Project Lab",
    full_name: "Internship Assessment / Mini Project Lab (BCC351)",
    course_type: "lab",
    faculty_name: "Er. Gopal Singh / Er. Hitendra Kumar Prajapati",
    room_or_lab: "Lab-06",
    target_group: "G2: Wed 03:11-04:50 (Lab-06) | G1: Fri 02:21-04:00 (Lab-06)",
    time_slot: "Wed 03:11-04:50 (G2) / Fri 02:21-04:00 (G1)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#E65100",
    icon: "🚀"
  }
];

export function calculateHaversine(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const toRad = x => x * Math.PI / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}
