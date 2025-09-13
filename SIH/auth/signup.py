# auth/signup.py
from data.datastore import users

def signup(username, password, role="patient"):
    """Register a new user. Default role = patient."""
    if username in users:
        return False  # already exists
    users[username] = {"password": password, "role": role}
    return True
