# controllers/therapy_controller.py
from data.datastore import therapies, audit_logs
from datetime import datetime

def add_therapy(user, patient_id, therapy_name):
    therapies.append({"patient_id": patient_id, "therapy_name": therapy_name})
    audit_logs.append({
        "user": user,
        "action": f"Added therapy {therapy_name} to patient {patient_id}",
        "timestamp": datetime.now().isoformat()
    })
