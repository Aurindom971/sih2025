import sys
from PyQt5.QtWidgets import QApplication

# Import your windows
from views.login_window import LoginWindow
from views.signup_window import SignupWindow      # for future signup window
from views.patient_window import PatientWindow
from views.doctor_window import DoctorWindow      # Doctor functionality included
from views.audit_window import AuditWindow        # Admin window
from data import datastore                        # ✅ to access admins list


class AppManager:
    """Central controller for switching between windows."""
    def __init__(self):
        # Create QApplication first
        self.app = QApplication(sys.argv)

        # Hold references so windows are not garbage collected
        self.login_window = None
        self.signup_window = None
        self.patient_window = None
        self.doctor_window = None
        self.audit_window = None

        # Start with login window
        self.show_login_window()

    # ---------------------- WINDOWS ---------------------- #
    def show_login_window(self):
        """Show the login window."""
        if self.login_window:
            self.login_window.close()

        self.login_window = LoginWindow(app_reference=self)
        self.login_window.show()

    def show_signup_window(self):
        """Show the signup window (if implemented later)."""
        if self.signup_window:
            self.signup_window.close()

        self.signup_window = SignupWindow(app_reference=self)
        self.signup_window.show()

    def show_patient_window(self, username):
        """Open patient window for a logged-in patient."""
        if self.patient_window:
            self.patient_window.close()

        self.patient_window = PatientWindow(app_reference=self, username=username)
        self.patient_window.show()

    def show_doctor_window(self, username):
        """Open doctor window for a logged-in doctor."""
        if self.doctor_window:
            self.doctor_window.close()

        self.doctor_window = DoctorWindow(app_reference=self, username=username)
        self.doctor_window.show()

    def show_audit_window(self, username):
        """Open audit window for a logged-in admin."""
        admin_user = next((a for a in datastore.admins if a["username"] == username), None)

        if not admin_user:
            print(f"[ERROR] Admin {username} not found in datastore")
            self.show_login_window()
            return

        if self.audit_window:
            self.audit_window.close()

        self.audit_window = AuditWindow(app_reference=self, admin_user=admin_user)
        self.audit_window.show()

    def show_dashboard(self, username, role):
        """Determine which window to open after login based on role."""
        role = role.lower()
        if role == "patient":
            self.show_patient_window(username)
        elif role == "doctor":
            self.show_doctor_window(username)
        elif role == "admin":
            self.show_audit_window(username)
        else:
            print(f"[ERROR] Unknown role for {username}: {role}")
            self.show_login_window()

    # ---------------------- APP RUNNER ---------------------- #
    def run(self):
        """Run the QApplication event loop."""
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    manager = AppManager()
    manager.run()
