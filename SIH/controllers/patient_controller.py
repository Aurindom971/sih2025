# controllers/patient_controller.py
from data.datastore import patients, audit_logs
from datetime import datetime

def add_patient(user, name, age):
    pid = len(patients) + 1
    patients.append({"id": pid, "name": name, "age": age})
    audit_logs.append({
        "user": user,
        "action": f"Added patient {name}",
        "timestamp": datetime.now().isoformat()
    })
    return pid
