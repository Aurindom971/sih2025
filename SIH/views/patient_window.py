# views/patient_window.py

import os
from PyQt5 import uic
from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
    QTableWidgetItem,
    QHeaderView
)
from data.datastore import patients, therapies, records


class PatientWindow(QDialog):
    def __init__(self, app_reference, username):
        super().__init__()
        self.app_reference = app_reference
        self.username = username

        # Load the patient UI file
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/patient.ui")
        uic.loadUi(ui_path, self)

        # Optional: set white background
        self.setStyleSheet("background-color: white;")

        # Populate patient details
        self.populate_patient_info()

        # Connect logout button
        if hasattr(self, "logoutButton"):
            self.logoutButton.clicked.connect(self.logout)

    def populate_patient_info(self):
        # Find the patient by username (id = username)
        patient = next((p for p in patients if p["username"] == self.username), None)

        if not patient:
            QMessageBox.warning(self, "Error", "Patient not found!")
            self.close()
            return

        # Set basic info labels
        if hasattr(self, "nameLabel"):
            self.nameLabel.setText(f"Name: {patient['name']}")
        if hasattr(self, "ageLabel"):
            self.ageLabel.setText(f"Age: {patient['age']}")
        if hasattr(self, "genderLabel"):
            self.genderLabel.setText(f"Gender: {patient['gender']}")
        if hasattr(self, "idLabel"):
            self.idLabel.setText(f"ID: {patient['id']}")
        if hasattr(self, "remarksLabel"):
            self.remarksLabel.setText(f"Remarks: {patient.get('patient_remarks', 'N/A')}")
        if hasattr(self, "medicinesLabel"):
            self.medicinesLabel.setText(f"Medicines: {patient.get('patient_medicines', 'N/A')}")

        # -----------------------
        # Fill therapies table
        # -----------------------
        patient_therapies = [t for t in therapies if t["patient_id"] == self.username]

        if hasattr(self, "therapyTable"):
            self.therapyTable.setColumnCount(2)
            self.therapyTable.setHorizontalHeaderLabels(["Therapy", "Sessions"])
            self.therapyTable.setRowCount(len(patient_therapies))

            for row, t in enumerate(patient_therapies):
                self.therapyTable.setItem(row, 0, QTableWidgetItem(t.get("therapy_name", "")))
                self.therapyTable.setItem(row, 1, QTableWidgetItem(str(t.get("sessions", 0))))

            # Stretch columns nicely
            self.therapyTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.therapyTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        # -----------------------
        # Fill records table
        # -----------------------
        patient_records = [r for r in records if r["patient_id"] == self.username]

        if hasattr(self, "recordTable"):
            self.recordTable.setColumnCount(1)
            self.recordTable.setHorizontalHeaderLabels(["Record"])
            self.recordTable.setRowCount(len(patient_records))

            for row, r in enumerate(patient_records):
                self.recordTable.setItem(row, 0, QTableWidgetItem(r.get("record", "")))

            # Stretch record column to full width
            self.recordTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def logout(self):
        """Close patient window, return to login, and show logout message."""
        self.close()
        if self.app_reference:
            self.app_reference.show_login_window()
        QMessageBox.information(self, "Logout", "Patient logged out successfully.")
