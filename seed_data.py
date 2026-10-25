import json
from .db import get_db_connection, init_db

FLOORS_DATA = [
    {"id": 0, "name": "Ground Floor", "elevation": 0.00, "height": 4.95, "description": "Admin, Principal Cabin, ED Sir Cabin, Central Library, MECH, Civil & Entrances"},
    {"id": 1, "name": "First Floor", "elevation": 4.95, "height": 4.05, "description": "Computer Science & Engineering (CSE) Department, Labs 51-59, Classrooms 4-10, HOD Cabin"},
    {"id": 2, "name": "Second Floor", "elevation": 9.00, "height": 3.50, "description": "AI & Data Science (AIDS), ECE, Electrical, Architecture (AR), Seminar Hall"}
]

STAIRCASES_DATA = [
    {
        "id": "STAIR_S1",
        "name": "Staircase S1 (South-West Core)",
        "stair_type": "stairs",
        "floors_connected": json.dumps([0, 1, 2]),
        "x": 20.5,
        "y": 7.0,
        "width": 8.47,
        "length": 4.5
    },
    {
        "id": "STAIR_S2",
        "name": "Staircase S2 (North-East Core)",
        "stair_type": "stairs",
        "floors_connected": json.dumps([0, 1, 2]),
        "x": 48.5,
        "y": 57.0,
        "width": 5.2,
        "length": 4.5
    },
    {
        "id": "LIFT_L1",
        "name": "Central Lift L1 (Courtyard Core)",
        "stair_type": "lift",
        "floors_connected": json.dumps([0, 1, 2]),
        "x": 39.9,
        "y": 17.5,
        "width": 1.8,
        "length": 1.8
    }
]

ROOMS_DATA = [
    # ------------------ Floor 0 (Ground) ------------------
    {
        "id": "MAIN_GATE",
        "name": "SITCOE Main Entrance / Porch",
        "room_number": "ENT-01",
        "floor_id": 0,
        "department": "Campus",
        "room_type": "Entrance",
        "x": 32.5, "y": 2.0, "z": 0.0,
        "door_x": 32.5, "door_y": 18.0,
        "width": 8.0, "length": 4.0, "area_sqm": 32.0,
        "info": "Main building entry porch connecting the portico to the central quadrangle.",
        "color": "#ef4444"
    },
    {
        "id": "ADMIN_PRINCIPAL",
        "name": "Principal's Cabin (Dr. Sanjay A. Khot)",
        "room_number": "Admin-01",
        "floor_id": 0,
        "department": "Admin",
        "room_type": "Admin",
        "x": 35.0, "y": 10.0, "z": 0.0,
        "door_x": 35.0, "door_y": 18.0,
        "width": 6.0, "length": 6.0, "area_sqm": 36.0,
        "info": "Office of Principal Dr. Sanjay A. Khot, SITCOE.",
        "color": "#ef4444"
    },
    {
        "id": "ADMIN_ED",
        "name": "Executive Director's Cabin (Hon. Anil A. Bagane)",
        "room_number": "Admin-02",
        "floor_id": 0,
        "department": "Admin",
        "room_type": "Admin",
        "x": 38.0, "y": 10.0, "z": 0.0,
        "door_x": 38.0, "door_y": 18.0,
        "width": 6.0, "length": 6.0, "area_sqm": 36.0,
        "info": "Office of Executive Director Hon. Anil A. Bagane (ED Sir).",
        "color": "#ef4444"
    },
    {
        "id": "ADMIN_BOARD",
        "name": "Board Room",
        "room_number": "Admin-03",
        "floor_id": 0,
        "department": "Admin",
        "room_type": "Admin",
        "x": 42.0, "y": 10.0, "z": 0.0,
        "door_x": 42.0, "door_y": 18.0,
        "width": 7.0, "length": 6.0, "area_sqm": 42.0,
        "info": "Executive Board Meeting Room.",
        "color": "#ef4444"
    },
    {
        "id": "ADMIN_OFFICE",
        "name": "Main Office & Registrar (Mr. S. M. Dhabade)",
        "room_number": "Admin-04",
        "floor_id": 0,
        "department": "Admin",
        "room_type": "Admin",
        "x": 28.0, "y": 10.0, "z": 0.0,
        "door_x": 28.0, "door_y": 18.0,
        "width": 8.0, "length": 6.0, "area_sqm": 48.0,
        "info": "Student administration, admissions, scholarships, and registrar office.",
        "color": "#ef4444"
    },
    {
        "id": "ADMIN_EXAM",
        "name": "Exam Cell Office",
        "room_number": "Admin-05",
        "floor_id": 0,
        "department": "Admin",
        "room_type": "Admin",
        "x": 46.0, "y": 10.0, "z": 0.0,
        "door_x": 46.0, "door_y": 18.0,
        "width": 6.0, "length": 6.0, "area_sqm": 36.0,
        "info": "University examinations, test scheduling, and grade control.",
        "color": "#ef4444"
    },
    {
        "id": "ADMIN_PLACEMENT",
        "name": "Training & Placement Cell",
        "room_number": "Admin-06",
        "floor_id": 0,
        "department": "Admin",
        "room_type": "Admin",
        "x": 48.0, "y": 10.0, "z": 0.0,
        "door_x": 48.0, "door_y": 18.0,
        "width": 6.0, "length": 5.0, "area_sqm": 30.0,
        "info": "Campus recruitment and placement office.",
        "color": "#ef4444"
    },
    {
        "id": "LIB_121",
        "name": "Central Library (Mr. P. B. More)",
        "room_number": "121",
        "floor_id": 0,
        "department": "Library",
        "room_type": "Library",
        "x": 58.0, "y": 35.0, "z": 0.0,
        "door_x": 49.2, "door_y": 35.0,
        "width": 12.0, "length": 14.0, "area_sqm": 168.0,
        "info": "Central academic library and reference section.",
        "color": "#10b981"
    },
    {
        "id": "LIB_DIGITAL",
        "name": "Digital Library Lab",
        "room_number": "122",
        "floor_id": 0,
        "department": "Library",
        "room_type": "Laboratory",
        "x": 58.0, "y": 42.0, "z": 0.0,
        "door_x": 49.2, "door_y": 42.0,
        "width": 10.0, "length": 6.3, "area_sqm": 63.38,
        "info": "Digital catalogue, IEEE research papers, and e-learning resources.",
        "color": "#10b981"
    },
    {
        "id": "MECH_201",
        "name": "Applied Thermodynamics Lab & HOD Mech (Dr. S. K. Jadhav)",
        "room_number": "201",
        "floor_id": 0,
        "department": "MECH",
        "room_type": "Laboratory",
        "x": 8.0, "y": 30.0, "z": 0.0,
        "door_x": 16.0, "door_y": 30.0,
        "width": 10.0, "length": 8.0, "area_sqm": 79.57,
        "info": "Mechanical Engineering HOD Cabin and Thermodynamics experimental lab.",
        "color": "#8b5cf6"
    },
    {
        "id": "MECH_202",
        "name": "Central Mechanical Workshop (Prof. A. L. Shinde)",
        "room_number": "202",
        "floor_id": 0,
        "department": "MECH",
        "room_type": "Laboratory",
        "x": 8.0, "y": 45.0, "z": 0.0,
        "door_x": 16.0, "door_y": 45.0,
        "width": 10.0, "length": 12.0, "area_sqm": 120.0,
        "info": "Manufacturing process machines, fitting, carpentry, and welding workshop.",
        "color": "#10b981"
    },
    {
        "id": "CIVIL_301",
        "name": "Surveying Lab & HOD Civil (Dr. R. V. Kulkarni)",
        "room_number": "301",
        "floor_id": 0,
        "department": "Civil",
        "room_type": "Laboratory",
        "x": 58.0, "y": 20.0, "z": 0.0,
        "door_x": 49.2, "door_y": 20.0,
        "width": 10.0, "length": 6.8, "area_sqm": 68.5,
        "info": "Civil Engineering HOD Cabin and total station / GPS surveying lab.",
        "color": "#8b5cf6"
    },
    {
        "id": "CLASS_01",
        "name": "Class Room 1",
        "room_number": "1",
        "floor_id": 0,
        "department": "First Year",
        "room_type": "Classroom",
        "x": 8.0, "y": 20.0, "z": 0.0,
        "door_x": 16.0, "door_y": 20.0,
        "width": 10.0, "length": 6.7, "area_sqm": 67.0,
        "info": "First Year Engineering Lecture Classroom 1.",
        "color": "#3b82f6"
    },
    {
        "id": "CLASS_02",
        "name": "Class Room 2",
        "room_number": "2",
        "floor_id": 0,
        "department": "First Year",
        "room_type": "Classroom",
        "x": 8.0, "y": 25.0, "z": 0.0,
        "door_x": 16.0, "door_y": 25.0,
        "width": 10.0, "length": 6.7, "area_sqm": 67.0,
        "info": "First Year Engineering Lecture Classroom 2.",
        "color": "#3b82f6"
    },

    # ------------------ Floor 1 (First Floor - CSE Wing) ------------------
    {
        "id": "CSE_ROOM_04",
        "name": "Class Room No. 4",
        "room_number": "4",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Classroom",
        "x": 8.0, "y": 19.5, "z": 4.95,
        "door_x": 16.0, "door_y": 19.5,
        "width": 10.0, "length": 6.65, "area_sqm": 66.50,
        "info": "Computer Science lecture classroom with smart projector.",
        "color": "#3b82f6"
    },
    {
        "id": "CSE_ROOM_05",
        "name": "Class Room No. 5",
        "room_number": "5",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Classroom",
        "x": 8.0, "y": 26.0, "z": 4.95,
        "door_x": 16.0, "door_y": 26.0,
        "width": 10.0, "length": 6.65, "area_sqm": 66.50,
        "info": "Computer Science lecture classroom with digital board.",
        "color": "#3b82f6"
    },
    {
        "id": "CSE_ROOM_06",
        "name": "Class Room No. 6",
        "room_number": "6",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Classroom",
        "x": 8.0, "y": 32.5, "z": 4.95,
        "door_x": 16.0, "door_y": 32.5,
        "width": 10.0, "length": 6.65, "area_sqm": 66.50,
        "info": "CSE Department Classroom 6.",
        "color": "#3b82f6"
    },
    {
        "id": "CSE_ROOM_07",
        "name": "Class Room No. 7",
        "room_number": "7",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Classroom",
        "x": 8.0, "y": 39.0, "z": 4.95,
        "door_x": 16.0, "door_y": 39.0,
        "width": 10.0, "length": 6.65, "area_sqm": 66.50,
        "info": "CSE Department Classroom 7.",
        "color": "#3b82f6"
    },
    {
        "id": "CSE_ROOM_08",
        "name": "Class Room No. 8",
        "room_number": "8",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Classroom",
        "x": 8.0, "y": 45.5, "z": 4.95,
        "door_x": 16.0, "door_y": 45.5,
        "width": 10.0, "length": 6.65, "area_sqm": 66.50,
        "info": "CSE Department Classroom 8.",
        "color": "#3b82f6"
    },
    {
        "id": "CSE_ROOM_38",
        "name": "VLSI & Embedded System Lab (Room 38 / Class 9)",
        "room_number": "38",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 8.0, "y": 53.0, "z": 4.95,
        "door_x": 16.0, "door_y": 50.0,
        "width": 10.0, "length": 10.24, "area_sqm": 102.40,
        "info": "VLSI design, FPGA boards, microcontrollers, and embedded kits lab.",
        "color": "#10b981"
    },
    {
        "id": "CSE_LAB_51",
        "name": "Database Laboratory",
        "room_number": "51",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 34.0, "y": 9.0, "z": 4.95,
        "door_x": 34.0, "door_y": 18.0,
        "width": 8.5, "length": 7.8, "area_sqm": 66.30,
        "info": "Relational Database Management Systems, SQL, MongoDB, and Big Data lab.",
        "color": "#10b981"
    },
    {
        "id": "CSE_LAB_52",
        "name": "Web Technology Laboratory",
        "room_number": "52",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 41.0, "y": 9.0, "z": 4.95,
        "door_x": 41.0, "door_y": 18.0,
        "width": 8.5, "length": 7.8, "area_sqm": 66.30,
        "info": "Full Stack Web Development, Cloud Computing, and API Engineering lab.",
        "color": "#10b981"
    },
    {
        "id": "CSE_LAB_54",
        "name": "Operating System Laboratory (Prof. P. Q. Deshmukh)",
        "room_number": "54",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 58.0, "y": 45.0, "z": 4.95,
        "door_x": 49.2, "door_y": 45.0,
        "width": 10.0, "length": 7.6, "area_sqm": 76.00,
        "info": "Linux kernel internals, OS process scheduling, and systems programming.",
        "color": "#10b981"
    },
    {
        "id": "CSE_LAB_55",
        "name": "Micro Processor Laboratory",
        "room_number": "55",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 58.0, "y": 39.0, "z": 4.95,
        "door_x": 49.2, "door_y": 39.0,
        "width": 10.0, "length": 6.75, "area_sqm": 67.50,
        "info": "8086 Assembly, ARM architecture, and hardware interfacing lab.",
        "color": "#10b981"
    },
    {
        "id": "CSE_LAB_56",
        "name": "Computer Network Laboratory",
        "room_number": "56",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 58.0, "y": 33.0, "z": 4.95,
        "door_x": 49.2, "door_y": 33.0,
        "width": 10.0, "length": 6.75, "area_sqm": 67.50,
        "info": "CISCO packet tracer, network routing protocols, and cybersecurity lab.",
        "color": "#10b981"
    },
    {
        "id": "CSE_LAB_58",
        "name": "Programming Laboratory (Prof. S. R. Mane)",
        "room_number": "58",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 58.0, "y": 27.0, "z": 4.95,
        "door_x": 49.2, "door_y": 27.0,
        "width": 10.0, "length": 7.6, "area_sqm": 76.00,
        "info": "Java Programming, Data Structures & Algorithms, and Python lab.",
        "color": "#10b981"
    },
    {
        "id": "CSE_LAB_59",
        "name": "Project Laboratory",
        "room_number": "59",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Laboratory",
        "x": 58.0, "y": 21.0, "z": 4.95,
        "door_x": 49.2, "door_y": 21.0,
        "width": 10.0, "length": 6.75, "area_sqm": 67.50,
        "info": "Final Year Capstone Projects and Innovation Incubator.",
        "color": "#10b981"
    },
    {
        "id": "CSE_HOD",
        "name": "HOD Office - Computer Science (Dr. A. B. Patil)",
        "room_number": "HOD-CSE",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "HOD Cabin",
        "x": 58.0, "y": 14.0, "z": 4.95,
        "door_x": 49.2, "door_y": 15.0,
        "width": 4.9, "length": 3.85, "area_sqm": 18.86,
        "info": "Cabin of Dr. A. B. Patil, Professor & Head of Department, CSE.",
        "color": "#8b5cf6"
    },
    {
        "id": "CSE_FACULTY_53A",
        "name": "Faculty Cabins 53A-53D",
        "room_number": "53A-D",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Faculty Cabin",
        "x": 47.0, "y": 9.0, "z": 4.95,
        "door_x": 47.0, "door_y": 18.0,
        "width": 5.57, "length": 3.96, "area_sqm": 22.05,
        "info": "Computer Science Faculty consultation cabins.",
        "color": "#8b5cf6"
    },
    {
        "id": "CSE_SERVER_53E",
        "name": "Campus Server Room (53E)",
        "room_number": "53E",
        "floor_id": 1,
        "department": "CSE",
        "room_type": "Admin",
        "x": 47.0, "y": 14.0, "z": 4.95,
        "door_x": 47.0, "door_y": 18.0,
        "width": 5.57, "length": 3.96, "area_sqm": 22.05,
        "info": "Campus high speed rack servers, firewall, and data center.",
        "color": "#ef4444"
    },

    # ------------------ Floor 2 (Second Floor) ------------------
    {
        "id": "AIDS_701",
        "name": "AI Lab & HOD AIDS (Dr. S. S. Kamble)",
        "room_number": "701",
        "floor_id": 2,
        "department": "AIDS",
        "room_type": "Laboratory",
        "x": 8.0, "y": 38.0, "z": 9.0,
        "door_x": 16.0, "door_y": 38.0,
        "width": 10.0, "length": 6.75, "area_sqm": 67.50,
        "info": "Artificial Intelligence & Data Science Department HOD and Machine Learning GPU Lab.",
        "color": "#8b5cf6"
    },
    {
        "id": "ECE_501",
        "name": "VLSI Lab & HOD ECE (Dr. M. M. Kamble)",
        "room_number": "501",
        "floor_id": 2,
        "department": "ECE",
        "room_type": "Laboratory",
        "x": 8.0, "y": 25.0, "z": 9.0,
        "door_x": 16.0, "door_y": 25.0,
        "width": 10.0, "length": 6.75, "area_sqm": 67.50,
        "info": "Electronics & Computer Engineering HOD Cabin and VLSI Design Lab.",
        "color": "#8b5cf6"
    },
    {
        "id": "AR_601",
        "name": "Robotics Lab & HOD Architecture (Dr. G. B. Chavan)",
        "room_number": "601",
        "floor_id": 2,
        "department": "AR",
        "room_type": "Laboratory",
        "x": 58.0, "y": 25.0, "z": 9.0,
        "door_x": 49.2, "door_y": 25.0,
        "width": 10.0, "length": 6.75, "area_sqm": 67.50,
        "info": "Architecture & Robotics Studio, CAD/BIM lab.",
        "color": "#8b5cf6"
    },
    {
        "id": "ELECT_401",
        "name": "Electrical Machines Lab & HOD (Dr. K. N. Joshi)",
        "room_number": "401",
        "floor_id": 2,
        "department": "Electrical",
        "room_type": "Laboratory",
        "x": 58.0, "y": 38.0, "z": 9.0,
        "door_x": 49.2, "door_y": 38.0,
        "width": 10.0, "length": 6.75, "area_sqm": 67.50,
        "info": "Electrical Engineering HOD Cabin and AC/DC Machines Lab.",
        "color": "#8b5cf6"
    },
    {
        "id": "SEMINAR_HALL",
        "name": "Auditorium & Central Seminar Hall",
        "room_number": "210",
        "floor_id": 2,
        "department": "Admin",
        "room_type": "Classroom",
        "x": 34.0, "y": 9.0, "z": 9.0,
        "door_x": 34.0, "door_y": 18.0,
        "width": 17.0, "length": 8.0, "area_sqm": 136.0,
        "info": "Air-conditioned seminar hall for conferences, hackathons, and guest lectures.",
        "color": "#3b82f6"
    }
]

FACULTY_DATA = [
    {
        "name": "Dr. A. B. Patil",
        "designation": "Professor & HOD",
        "department": "CSE",
        "cabin_room_id": "CSE_HOD",
        "cabin_name": "HOD Office (Floor 1)",
        "floor_id": 1,
        "subject": "Computer Networks & Wireless Communication"
    },
    {
        "name": "Prof. P. Q. Deshmukh",
        "designation": "Assistant Professor",
        "department": "CSE",
        "cabin_room_id": "CSE_LAB_54",
        "cabin_name": "Operating System Laboratory (Room 54, Floor 1)",
        "floor_id": 1,
        "subject": "Operating Systems & Linux Kernel"
    },
    {
        "name": "Prof. S. R. Mane",
        "designation": "Assistant Professor",
        "department": "CSE",
        "cabin_room_id": "CSE_LAB_58",
        "cabin_name": "Programming Laboratory (Room 58, Floor 1)",
        "floor_id": 1,
        "subject": "Java Programming & Data Structures"
    },
    {
        "name": "Dr. S. K. Jadhav",
        "designation": "Professor & HOD",
        "department": "MECH",
        "cabin_room_id": "MECH_201",
        "cabin_name": "Thermal Lab (Room 201, Floor 0)",
        "floor_id": 0,
        "subject": "Thermodynamics & Heat Transfer"
    },
    {
        "name": "Prof. A. L. Shinde",
        "designation": "Assistant Professor",
        "department": "MECH",
        "cabin_room_id": "MECH_202",
        "cabin_name": "Workshop Room (Room 202, Floor 0)",
        "floor_id": 0,
        "subject": "Manufacturing Engineering"
    },
    {
        "name": "Dr. R. V. Kulkarni",
        "designation": "Professor & HOD",
        "department": "Civil",
        "cabin_room_id": "CIVIL_301",
        "cabin_name": "Survey Office (Room 301, Floor 0)",
        "floor_id": 0,
        "subject": "Surveying & Building Planning"
    },
    {
        "name": "Dr. K. N. Joshi",
        "designation": "Professor & HOD",
        "department": "Electrical",
        "cabin_room_id": "ELECT_401",
        "cabin_name": "Machine Cabin (Room 401, Floor 2)",
        "floor_id": 2,
        "subject": "Electrical Machines & Power Systems"
    },
    {
        "name": "Dr. M. M. Kamble",
        "designation": "Professor & HOD",
        "department": "ECE",
        "cabin_room_id": "ECE_501",
        "cabin_name": "VLSI Cabin (Room 501, Floor 2)",
        "floor_id": 2,
        "subject": "VLSI Systems & Microprocessors"
    },
    {
        "name": "Dr. G. B. Chavan",
        "designation": "Professor & HOD",
        "department": "AR",
        "cabin_room_id": "AR_601",
        "cabin_name": "Robotics Design (Room 601, Floor 2)",
        "floor_id": 2,
        "subject": "Automation Systems & Architectural Robotics"
    },
    {
        "name": "Dr. S. S. Kamble",
        "designation": "Professor & HOD",
        "department": "AIDS",
        "cabin_room_id": "AIDS_701",
        "cabin_name": "AI Room (Room 701, Floor 2)",
        "floor_id": 2,
        "subject": "Artificial Intelligence & Data Science"
    },
    {
        "name": "Mr. P. B. More",
        "designation": "Librarian",
        "department": "Library",
        "cabin_room_id": "LIB_121",
        "cabin_name": "Central Library (Room 121, Floor 0)",
        "floor_id": 0,
        "subject": "Information Management"
    },
    {
        "name": "Dr. Sanjay A. Khot",
        "designation": "Principal",
        "department": "Admin",
        "cabin_room_id": "ADMIN_PRINCIPAL",
        "cabin_name": "Principal's Cabin (Floor 0)",
        "floor_id": 0,
        "subject": "Administration & Campus Leadership"
    },
    {
        "name": "Hon. Anil A. Bagane",
        "designation": "Executive Director (ED Sir)",
        "department": "Admin",
        "cabin_room_id": "ADMIN_ED",
        "cabin_name": "ED Sir's Cabin (Floor 0)",
        "floor_id": 0,
        "subject": "Strategic Trust Management"
    },
    {
        "name": "Mr. S. M. Dhabade",
        "designation": "Registrar / Administrative Officer",
        "department": "Admin",
        "cabin_room_id": "ADMIN_OFFICE",
        "cabin_name": "Main Office (Floor 0)",
        "floor_id": 0,
        "subject": "Campus Records, Admissions & Finance"
    }
]

EMERGENCY_DATA = [
    {
        "id": "HOSPITAL",
        "name": "Sharad Ayurved Hospital (Yadrav)",
        "service_type": "Hospital",
        "phone": "02322-253000",
        "description": "24/7 Emergency medical care adjacent to SITCOE campus.",
        "latitude": 16.70582,
        "longitude": 74.47563
    },
    {
        "id": "POLICE",
        "name": "Shivaji Nagar Police Station",
        "service_type": "Police",
        "phone": "0230-2432000",
        "description": "Serving Yadrav/Ichalkaranji municipal region.",
        "latitude": 16.68551,
        "longitude": 74.45861
    }
]

def seed_database():
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()

    # Clear existing
    cur.execute("DELETE FROM faculty")
    cur.execute("DELETE FROM rooms")
    cur.execute("DELETE FROM staircases")
    cur.execute("DELETE FROM floors")
    cur.execute("DELETE FROM emergency_services")

    # Insert Floors
    for f in FLOORS_DATA:
        cur.execute(
            "INSERT INTO floors (id, name, elevation, height, description) VALUES (?, ?, ?, ?, ?)",
            (f["id"], f["name"], f["elevation"], f["height"], f["description"])
        )

    # Insert Staircases
    for s in STAIRCASES_DATA:
        cur.execute(
            "INSERT INTO staircases (id, name, stair_type, floors_connected, x, y, width, length) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (s["id"], s["name"], s["stair_type"], s["floors_connected"], s["x"], s["y"], s["width"], s["length"])
        )

    # Insert Rooms
    for r in ROOMS_DATA:
        cur.execute(
            """INSERT INTO rooms (id, name, room_number, floor_id, department, room_type, x, y, z, door_x, door_y, width, length, area_sqm, info, color)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                r["id"], r["name"], r.get("room_number"), r["floor_id"], r["department"], r["room_type"],
                r["x"], r["y"], r["z"], r["door_x"], r["door_y"],
                r.get("width"), r.get("length"), r.get("area_sqm"), r.get("info"), r.get("color", "#3b82f6")
            )
        )

    # Insert Faculty
    for fac in FACULTY_DATA:
        cur.execute(
            """INSERT INTO faculty (name, designation, department, cabin_room_id, cabin_name, floor_id, subject)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (fac["name"], fac["designation"], fac["department"], fac["cabin_room_id"], fac["cabin_name"], fac["floor_id"], fac.get("subject"))
        )

    # Insert Emergency Services
    for em in EMERGENCY_DATA:
        cur.execute(
            """INSERT INTO emergency_services (id, name, service_type, phone, description, latitude, longitude)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (em["id"], em["name"], em["service_type"], em["phone"], em["description"], em["latitude"], em["longitude"])
        )

    conn.commit()
    conn.close()
    print("Database successfully seeded with SITCOE verified CAD and campus data!")

if __name__ == "__main__":
    seed_database()
