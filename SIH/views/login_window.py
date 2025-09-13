# views/login_window.py

import sys
import os

import sys
import os
from PyQt5.QtCore import Qt
# Add project root (SIH/) to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFrame

from auth.login import authenticate  # type: ignore # This should now work


class LoginWindow(QDialog):
    def __init__(self, app_reference):
        super().__init__()

        # Correct path to login.ui
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "login.ui")
        if not os.path.exists(ui_path):
            raise FileNotFoundError(f"UI file not found at: {ui_path}")

        uic.loadUi(ui_path, self)

        # Optional: set a frame style if you have a frame in the UI
        if hasattr(self, "loginFrame"):
            self.loginFrame.setFrameShape(QFrame.Box)
            self.loginFrame.setFrameShadow(QFrame.Plain)

        self.app_reference = app_reference

        # Connect buttons
        self.loginButton.clicked.connect(self.handle_login)
        self.signupButton.clicked.connect(self.open_signup)

        # Show window
        self.show()

    def handle_login(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()

        # Determine selected role from radio buttons
        if self.doctorRadio.isChecked():
            role = "doctor"
        elif self.patientRadio.isChecked():
            role = "patient"
        elif self.adminRadio.isChecked():
            role = "admin"
        else:
            self.statusLabel.setText("Please select a role")
            return  # stop if no role selected

        # Authenticate based on selected role
        if authenticate(username, password, role):  # your authenticate now expects role
            self.app_reference.show_dashboard(username, role)
            self.close()
        else:
            self.statusLabel.setText("Invalid credentials")

    def open_signup(self):
        self.app_reference.show_signup_window()
        self.close()
