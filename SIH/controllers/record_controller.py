# controllers/record_controller.py
from data.datastore import records, audit_logs
from datetime import datetime

def add_record(user, patient_id, record_text):
    records.append({"patient_id": patient_id, "record": record_text})
    audit_logs.append({
        "user": user,
        "action": f"Added record for patient {patient_id}",
        "timestamp": datetime.now().isoformat()
    })

def get_patient_records(patient_id):
    return [r for r in records if r["patient_id"] == patient_id]
