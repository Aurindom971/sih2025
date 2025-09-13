# views/signup_window.py

import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFrame

# Make sure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your signup logic (you’ll need to implement it)
# For now, we’ll mock it
def register_user(username, password):
    # TODO: replace with real signup logic (DB insert)
    # Return True if signup successful, False otherwise
    return True

class SignupWindow(QDialog):
    def __init__(self, app_reference):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "signup.ui")
        if not os.path.exists(ui_path):
            raise FileNotFoundError(f"UI file not found at: {ui_path}")

        uic.loadUi(ui_path, self)

        # Optional: Frame styling
        if hasattr(self, "signupFrame"):
            self.signupFrame.setFrameShape(QFrame.Box)
            self.signupFrame.setFrameShadow(QFrame.Plain)
            self.signupFrame.setStyleSheet("""
                background-color: #ffffff;
                border-radius: 15px;
                border: 1px solid #cccccc;
            """)

        self.app_reference = app_reference

        # Connect buttons
        self.signupButton.clicked.connect(self.handle_signup)
        self.backButton.clicked.connect(self.back_to_login)

        # Show the window
        self.show()

    def handle_signup(self):
        username = self.usernameEdit.text().strip()
        password = self.passwordEdit.text().strip()
        confirm = self.confirmPasswordEdit.text().strip()

        if password != confirm:
            self.statusLabel.setText("Passwords do not match")
            self.statusLabel.setStyleSheet("color: red;")
            return

        if register_user(username, password):
            self.statusLabel.setText("Signup successful!")
            self.statusLabel.setStyleSheet("color: green;")
            # Optionally, redirect back to login after success
            self.app_reference.show_login_window()
            self.close()
        else:
            self.statusLabel.setText("Signup failed")
            self.statusLabel.setStyleSheet("color: red;")

    def back_to_login(self):
        self.app_reference.show_login_window()
        self.close()
