# views/doctor_window.py

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from data.datastore import doctors, patients, therapies

class DoctorWindow(QDialog):
    def __init__(self, app_reference, username):
        super().__init__()
        self.app_reference = app_reference
        self.username = username

        # Load the correct UI file
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/doctor.ui")
        uic.loadUi(ui_path, self)

        # Find the doctor object
        self.doctor = next((d for d in doctors if d["username"] == username), None)
        if not self.doctor:
            QMessageBox.warning(self, "Error", f"Doctor '{username}' not found!")
            self.close()
            return

        # Set up UI with doctor info
        self.load_doctor_info()
        self.load_patients()

        # Connect buttons safely
        if hasattr(self, "logoutButton"):
            self.logoutButton.clicked.connect(self.logout)
        if hasattr(self, "addRowButton"):
            self.addRowButton.clicked.connect(self.add_patient_row)
        if hasattr(self, "saveButton"):
            self.saveButton.clicked.connect(self.save_patients)
        if hasattr(self, "deleteButton"):
            self.deleteButton.clicked.connect(self.delete_selected_row)

        # Make table editable only on double-click
        if hasattr(self, "patientsTable"):
            self.patientsTable.setEditTriggers(self.patientsTable.DoubleClicked)
            self.patientsTable.resizeColumnsToContents()  # auto-adjust column widths

    def load_doctor_info(self):
        """Set doctor info labels."""
        if hasattr(self, "labelDoctorID"):
            self.labelDoctorID.setText(self.doctor.get("id", "N/A"))
        if hasattr(self, "labelDoctorName"):
            self.labelDoctorName.setText(self.doctor.get("name", "N/A"))
        if hasattr(self, "labelDoctorField"):
            self.labelDoctorField.setText(self.doctor.get("doctor_field", "N/A"))
        if hasattr(self, "labelDoctorExperience"):
            self.labelDoctorExperience.setText(self.doctor.get("experience", "N/A"))

    def load_patients(self):
        """Load patients assigned to this doctor."""
        my_patients = [p for p in patients if p["doctor_id"] == self.username]

        if not hasattr(self, "patientsTable"):
            return

        self.patientsTable.setRowCount(len(my_patients))
        self.patientsTable.setColumnCount(6)
        self.patientsTable.setHorizontalHeaderLabels(
            ["Name", "Age", "Gender", "Medicines", "Remarks", "Therapy"]
        )

        for row, patient in enumerate(my_patients):
            therapy_name = next(
                (t["therapy_name"] for t in therapies if t["patient_id"] == patient["id"]), ""
            )
            self.patientsTable.setItem(row, 0, QTableWidgetItem(patient["name"]))
            self.patientsTable.setItem(row, 1, QTableWidgetItem(str(patient["age"])))
            self.patientsTable.setItem(row, 2, QTableWidgetItem(patient["gender"]))
            self.patientsTable.setItem(row, 3, QTableWidgetItem(patient.get("patient_medicines", "")))
            self.patientsTable.setItem(row, 4, QTableWidgetItem(patient.get("patient_remarks", "")))
            self.patientsTable.setItem(row, 5, QTableWidgetItem(therapy_name))

        # Auto-adjust column widths to fit content
        self.patientsTable.resizeColumnsToContents()

    def add_patient_row(self):
        """Add a blank row to enter a new patient."""
        if hasattr(self, "patientsTable"):
            self.patientsTable.insertRow(self.patientsTable.rowCount())

    def save_patients(self):
        """Save edited or newly added patients back to the datastore."""
        if not hasattr(self, "patientsTable"):
            return

        for row in range(self.patientsTable.rowCount()):
            name_item = self.patientsTable.item(row, 0)
            age_item = self.patientsTable.item(row, 1)
            gender_item = self.patientsTable.item(row, 2)
            medicines_item = self.patientsTable.item(row, 3)
            remarks_item = self.patientsTable.item(row, 4)
            therapy_item = self.patientsTable.item(row, 5)

            if not name_item or not age_item:
                continue

            patient_id = f"{self.username}_{row}"

            # Update or add patient
            existing = next((p for p in patients if p["id"] == patient_id), None)
            if existing:
                existing.update({
                    "name": name_item.text(),
                    "age": int(age_item.text()),
                    "gender": gender_item.text() if gender_item else "",
                    "patient_medicines": medicines_item.text() if medicines_item else "",
                    "patient_remarks": remarks_item.text() if remarks_item else ""
                })
            else:
                patients.append({
                    "id": patient_id,
                    "username": patient_id,
                    "password": "",
                    "name": name_item.text(),
                    "age": int(age_item.text()),
                    "gender": gender_item.text() if gender_item else "",
                    "doctor_id": self.username,
                    "patient_medicines": medicines_item.text() if medicines_item else "",
                    "patient_remarks": remarks_item.text() if remarks_item else ""
                })

            # Update or add therapy
            existing_therapy = next((t for t in therapies if t["patient_id"] == patient_id), None)
            if existing_therapy and therapy_item:
                existing_therapy["therapy_name"] = therapy_item.text()
            elif therapy_item:
                therapies.append({"patient_id": patient_id, "therapy_name": therapy_item.text(), "sessions": 0})

        QMessageBox.information(self, "Saved", "Patient data saved successfully!")
        # Adjust column widths after save
        self.patientsTable.resizeColumnsToContents()

    def delete_selected_row(self):
        """Delete selected patient rows."""
        if not hasattr(self, "patientsTable"):
            return

        selected_rows = self.patientsTable.selectionModel().selectedRows()
        for model_index in selected_rows:
            row = model_index.row()
            name_item = self.patientsTable.item(row, 0)
            if name_item:
                patient_name = name_item.text()
                patients[:] = [p for p in patients if p["name"] != patient_name]
                therapies[:] = [t for t in therapies if t["patient_id"] != f"{self.username}_{row}"]

            self.patientsTable.removeRow(row)

    def logout(self):
        """Close window, return to login, and show logout message."""
        self.close()
        if self.app_reference:
            self.app_reference.show_login_window()
        QMessageBox.information(self, "Logout", "Doctor logged out successfully.")
