# -------------------------------
# Doctors list
# -------------------------------
doctors = [
    {
        "id": "SIHD01",  # id is also the username
        "username": "SIHD01",
        "password": "docpass1",
        "name": "Dr. A. Sharma",
        "doctor_field": "Alopathic",
        "experience": "10 years"
    },
    {
        "id": "SIHD02",
        "username": "SIHD02",
        "password": "docpass2",
        "name": "Dr. B. Verma",
        "doctor_field": "Yoga Therapy",
        "experience": "7 years"
    }
]

# -------------------------------
# Patients list
# -------------------------------
patients = [
    {
        "id": "SIHP01",  # id is also the username
        "username": "SIHP01",
        "password": "patpass1",
        "name": "John Doe",
        "age": 30,
        "gender": "Male",
        "doctor_id": "SIHD01",
        "patient_remarks": "Diabetic",
        "patient_medicines": "Metformin"
    },
    {
        "id": "SIHP02",
        "username": "SIHP02",
        "password": "patpass2",
        "name": "Jane Smith",
        "age": 28,
        "gender": "Female",
        "doctor_id": "SIHD02",
        "patient_remarks": "Hypertensive",
        "patient_medicines": "Amlodipine"
    }
]

# -------------------------------
# Admins list
# -------------------------------
admins = [
    {
        "id": "admin1",
        "username": "admin1",
        "password": "adminpass1",
        "name": "System Admin"
    }
]

# -------------------------------
# Therapies list
# -------------------------------
therapies = [
    {"patient_id": "SIHP01", "therapy_name": "Panchakarma",  "sessions": 5},
    {"patient_id": "SIHP02", "therapy_name": "Yoga Therapy", "sessions": 10}
]

# -------------------------------
# Records list
# -------------------------------
records = [
    {"patient_id": "SIHP01", "record": "Blood test: Normal"},
    {"patient_id": "SIHP01", "record": "X-Ray: Mild issue"},
    {"patient_id": "SIHP01", "record": "Allergy test: Positive"}
]

# -------------------------------
# Audit logs
# -------------------------------
audit_logs = [
    {"user": "SIHD01", "action": "Added patient John Doe", "timestamp": "2025-09-13 10:00"},
    {"user": "SIHD02", "action": "Updated therapy for Jane Smith", "timestamp": "2025-09-13 11:00"},
    {"user": "admin1",  "action": "Viewed audit logs",       "timestamp": "2025-09-13 12:00"}
]


