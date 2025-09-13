# auth/login_logic.py
from data.datastore import doctors, patients, admins

def authenticate(username, password, role):
    """
    Check username, password and role in the correct list.
    Return the user profile dict if valid, else None.
    """
    if role == "doctor":
        for doc in doctors:
            if doc["username"] == username and doc["password"] == password:
                return doc  # full profile
    elif role == "patient":
        for pat in patients:
            if pat["username"] == username and pat["password"] == password:
                return pat
    elif role == "admin":
        for adm in admins:
            if adm["username"] == username and adm["password"] == password:
                return adm
    return None
