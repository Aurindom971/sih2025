# controllers/audit_controller.py
from data.datastore import audit_logs

def get_audit_logs():
    return audit_logs
