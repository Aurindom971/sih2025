import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from data import datastore


class AuditWindow(QtWidgets.QDialog):
    """
    Main Admin/Audit window:
    - Shows admin info + audit logs
    - Opens Doctor and Patient tabs
    """
    def __init__(self, admin_user, app_reference=None):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/audit.ui")
        uic.loadUi(ui_path, self)

        # Store references
        self.app_reference = app_reference
        self.admin_user = admin_user  # admin_user is already a dict

        # Set admin info safely
        self.labelAdminID.setText(self.admin_user.get("id", "Unknown"))
        self.labelAdminName.setText(self.admin_user.get("name", "Unknown"))

        # Load logs
        self.load_audit_logs()

        # Connect buttons
        self.doctorDetailsButton.clicked.connect(self.open_doctor_tab)
        self.patientDetailsButton.clicked.connect(self.open_patient_tab)
        self.logoutButton.clicked.connect(self.logout)

        # Child windows
        self.doctor_window = None
        self.patient_window = None

    # ----------------------
    # Load the audit logs
    # ----------------------
    def load_audit_logs(self):
        logs = datastore.audit_logs
        self.auditLogTable.setRowCount(len(logs))
        self.auditLogTable.setColumnCount(3)
        self.auditLogTable.setHorizontalHeaderLabels(["User", "Action", "Timestamp"])

        for row, log in enumerate(logs):
            self.auditLogTable.setItem(row, 0, QTableWidgetItem(log["user"]))
            self.auditLogTable.setItem(row, 1, QTableWidgetItem(log["action"]))
            self.auditLogTable.setItem(row, 2, QTableWidgetItem(log["timestamp"]))

        # Auto-adjust columns
        self.auditLogTable.resizeColumnsToContents()
        self.auditLogTable.horizontalHeader().setStretchLastSection(True)

        # If alertTable exists, do the same
        if hasattr(self, "alertTable"):
            self.alertTable.resizeColumnsToContents()
            self.alertTable.horizontalHeader().setStretchLastSection(True)

    # ----------------------
    # Doctor tab
    # ----------------------
    def open_doctor_tab(self):
        if not self.doctor_window:
            self.doctor_window = DoctorTabWindow(self.admin_user, self)
        self.doctor_window.show()

    # ----------------------
    # Patient tab
    # ----------------------
    def open_patient_tab(self):
        if not self.patient_window:
            self.patient_window = PatientTabWindow(self.admin_user, self)
        self.patient_window.show()

    # ----------------------
    # Logout
    # ----------------------
    def logout(self):
        self.close()
        if self.app_reference:
            self.app_reference.show_login_window()
        QMessageBox.information(self, "Logout", "Admin logged out successfully.")


# ==================================================
# DoctorTabWindow
# ==================================================
class DoctorTabWindow(QtWidgets.QDialog):
    """Doctor management tab for admin."""
    def __init__(self, admin_user, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/doctor_tab.ui")
        uic.loadUi(ui_path, self)

        self.admin_user = admin_user
        self.labelAdminID.setText(admin_user.get("id", "Unknown"))
        self.labelAdminName.setText(admin_user.get("name", "Unknown"))

        # Connect buttons
        self.logoutButton.clicked.connect(self.close)
        self.addDoctorRowButton.clicked.connect(self.add_row)
        self.saveDoctorButton.clicked.connect(self.save_changes)
        self.deleteDoctorRowButton.clicked.connect(self.delete_row)

        self.doctorTable.setColumnCount(5)
        self.doctorTable.setHorizontalHeaderLabels(
            ["Doctor ID", "Name", "Field", "Experience", "Assigned Patients"]
        )

        self.load_doctors()

    def load_doctors(self):
        """Load doctors into table."""
        docs = datastore.doctors
        self.doctorTable.setRowCount(len(docs))
        for row, doc in enumerate(docs):
            assigned_patients = ", ".join(
                [p["name"] for p in datastore.patients if p["doctor_id"] == doc["id"]]
            )
            self.doctorTable.setItem(row, 0, QTableWidgetItem(doc["id"]))
            self.doctorTable.setItem(row, 1, QTableWidgetItem(doc["name"]))
            self.doctorTable.setItem(row, 2, QTableWidgetItem(doc["doctor_field"]))
            self.doctorTable.setItem(row, 3, QTableWidgetItem(doc["experience"]))
            self.doctorTable.setItem(row, 4, QTableWidgetItem(assigned_patients))

        # Auto-adjust columns
        self.doctorTable.resizeColumnsToContents()
        self.doctorTable.horizontalHeader().setStretchLastSection(True)

    def add_row(self):
        self.doctorTable.insertRow(self.doctorTable.rowCount())

    def save_changes(self):
        new_doctors = []
        for row in range(self.doctorTable.rowCount()):
            doc_id = self.doctorTable.item(row, 0)
            name = self.doctorTable.item(row, 1)
            field = self.doctorTable.item(row, 2)
            exp = self.doctorTable.item(row, 3)

            if doc_id and name:
                new_doctors.append({
                    "id": doc_id.text(),
                    "username": doc_id.text(),
                    "password": "defaultpass",
                    "name": name.text(),
                    "doctor_field": field.text() if field else "",
                    "experience": exp.text() if exp else ""
                })

        datastore.doctors = new_doctors
        self.load_doctors()
        QMessageBox.information(self, "Saved", "Doctors list updated successfully!")

    def delete_row(self):
        current_row = self.doctorTable.currentRow()
        if current_row >= 0:
            self.doctorTable.removeRow(current_row)


# ==================================================
# PatientTabWindow
# ==================================================
class PatientTabWindow(QtWidgets.QDialog):
    """Patient management tab for admin."""
    def __init__(self, admin_user, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(__file__), "../ui/patient_tab.ui")
        uic.loadUi(ui_path, self)

        self.admin_user = admin_user
        self.labelAdminID.setText(admin_user.get("id", "Unknown"))
        self.labelAdminName.setText(admin_user.get("name", "Unknown"))

        # Connect buttons
        self.logoutButton.clicked.connect(self.close)
        self.addPatientRowButton.clicked.connect(self.add_row)
        self.savePatientButton.clicked.connect(self.save_changes)
        self.deletePatientRowButton.clicked.connect(self.delete_row)

        self.patientTable.setColumnCount(8)
        self.patientTable.setHorizontalHeaderLabels(
            ["Patient ID", "Name", "Age", "Gender", "Medicines",
             "Remarks", "Therapy", "Assigned Doctor"]
        )

        self.load_patients()

    def load_patients(self):
        pats = datastore.patients
        self.patientTable.setRowCount(len(pats))
        for row, pat in enumerate(pats):
            therapy = next((t["therapy_name"]
                            for t in datastore.therapies if t["patient_id"] == pat["id"]), "")
            self.patientTable.setItem(row, 0, QTableWidgetItem(pat["id"]))
            self.patientTable.setItem(row, 1, QTableWidgetItem(pat["name"]))
            self.patientTable.setItem(row, 2, QTableWidgetItem(str(pat["age"])))
            self.patientTable.setItem(row, 3, QTableWidgetItem(pat["gender"]))
            self.patientTable.setItem(row, 4, QTableWidgetItem(pat.get("patient_medicines", "")))
            self.patientTable.setItem(row, 5, QTableWidgetItem(pat.get("patient_remarks", "")))
            self.patientTable.setItem(row, 6, QTableWidgetItem(therapy))
            self.patientTable.setItem(row, 7, QTableWidgetItem(pat["doctor_id"]))

        # Auto-adjust columns
        self.patientTable.resizeColumnsToContents()
        self.patientTable.horizontalHeader().setStretchLastSection(True)

    def add_row(self):
        self.patientTable.insertRow(self.patientTable.rowCount())

    def save_changes(self):
        new_patients = []
        for row in range(self.patientTable.rowCount()):
            pat_id = self.patientTable.item(row, 0)
            name = self.patientTable.item(row, 1)
            age = self.patientTable.item(row, 2)
            gender = self.patientTable.item(row, 3)
            meds = self.patientTable.item(row, 4)
            remarks = self.patientTable.item(row, 5)
            therapy = self.patientTable.item(row, 6)
            doctor_id = self.patientTable.item(row, 7)

            if pat_id and name:
                new_patients.append({
                    "id": pat_id.text(),
                    "username": pat_id.text(),
                    "password": "defaultpass",
                    "name": name.text(),
                    "age": int(age.text()) if age and age.text().isdigit() else 0,
                    "gender": gender.text() if gender else "",
                    "doctor_id": doctor_id.text() if doctor_id else "",
                    "patient_remarks": remarks.text() if remarks else "",
                    "patient_medicines": meds.text() if meds else ""
                })

                # also update therapy separately
                if therapy and therapy.text():
                    existing = next((t for t in datastore.therapies
                                     if t["patient_id"] == pat_id.text()), None)
                    if existing:
                        existing["therapy_name"] = therapy.text()
                    else:
                        datastore.therapies.append({
                            "patient_id": pat_id.text(),
                            "therapy_name": therapy.text(),
                            "sessions": 0
                        })

        datastore.patients = new_patients
        self.load_patients()
        QMessageBox.information(self, "Saved", "Patients list updated successfully!")


    def delete_row(self):
        current_row = self.patientTable.currentRow()
        if current_row >= 0:
            self.patientTable.removeRow(current_row)


# ==================================================
# Standalone test
# ==================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    admin_user = datastore.admins[0]
    window = AuditWindow(admin_user)
    window.show()
    sys.exit(app.exec_())
