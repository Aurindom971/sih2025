# views/dashboard_window.py
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class DashboardWindow(QMainWindow):
    def __init__(self, app_reference, username, role):
        super().__init__()
        uic.loadUi("ui/dashboard.ui", self)
        self.app_reference = app_reference
        self.username = username
        self.role = role
        self.setup_buttons()

    def setup_buttons(self):
        if self.role == "doctor":
            self.patientButton.clicked.connect(lambda: self.app_reference.show_patient_window(self.username))
            self.therapyButton.clicked.connect(lambda: self.app_reference.show_therapy_window(self.username))
            self.recordButton.clicked.connect(lambda: self.app_reference.show_record_window(self.username))
        elif self.role == "patient":
            self.recordButton.clicked.connect(lambda: self.app_reference.show_record_window(self.username))
            self.patientButton.setDisabled(True)
            self.therapyButton.setDisabled(True)
        elif self.role == "admin":
            self.auditButton.clicked.connect(lambda: self.app_reference.show_audit_window())
            self.patientButton.setDisabled(True)
            self.therapyButton.setDisabled(True)
            self.recordButton.setDisabled(True)
