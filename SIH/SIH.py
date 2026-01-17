import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QLineEdit,
                               QTableWidget, QTableWidgetItem, QMessageBox)
from PySide6.QtCore import Qt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import random

# MongoDB Connection

class HospitalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Records Management")
        self.setGeometry(100, 100, 900, 600)

        self.logged_in_doctor = None
        self.logged_in_patient = None
        self.selected_patient = None
        self.patient_detail_origin = "doctor"

        self.stack = QWidget()
        self.stack_layout = QVBoxLayout()
        self.stack.setLayout(self.stack_layout)
        self.setCentralWidget(self.stack)

        self.pages = {}

        # Initialize all pages
        self.init_role_selection_page()
        self.init_doctor_login_page()
        self.init_patient_login_page()
        self.init_admin_login_page()
        self.init_admin_management_page()
        self.init_all_doctors_page()
        self.init_all_patients_page()
        self.init_new_doctor_page()
        self.init_new_patient_page()
        self.init_doctor_dashboard()
        self.init_patient_detail_page()
        self.init_patient_dashboard()

        self.set_page("role_selection")

    def clear_stack(self):
        for i in reversed(range(self.stack_layout.count())):
            widget = self.stack_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def set_page(self, name):
        self.clear_stack()
        page = self.pages.get(name)
        if page:
            self.stack_layout.addWidget(page)
            page.show()

    # --- View Patient and Doctor Records ---
    def load_all_doctors(self):
        doctors = list(db['Doctor_Info'].find({}, {'_id': 0}))
        self.all_doctors_table.setRowCount(len(doctors))
        for row, doctor in enumerate(doctors):
            self.all_doctors_table.setItem(row, 0, QTableWidgetItem(doctor.get('SRN', '')))
            self.all_doctors_table.setItem(row, 1, QTableWidgetItem(doctor.get('DoctorName', '')))
            self.all_doctors_table.setItem(row, 2, QTableWidgetItem(doctor.get('DoctorField', '')))
            self.all_doctors_table.setItem(row, 3, QTableWidgetItem(str(doctor.get('Experience', ''))))
        self.set_page("all_doctors")

    def load_all_patients(self):
        patients = list(db['Patient_Info'].find({}, {'_id': 0}))
        self.all_patients_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            self.all_patients_table.setItem(row, 0, QTableWidgetItem(patient.get('PSRN', '')))
            self.all_patients_table.setItem(row, 1, QTableWidgetItem(patient.get('PatientName', '')))
            self.all_patients_table.setItem(row, 2, QTableWidgetItem(patient.get('DoctorSRN', '')))
            self.all_patients_table.setItem(row, 3, QTableWidgetItem(str(patient.get('PatientAge', ''))))
            self.all_patients_table.setItem(row, 4, QTableWidgetItem(patient.get('PatientGender', '')))
        self.set_page("all_patients")

    # ------- Role Selection Page -------
    def init_role_selection_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Select Role to Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        btn_doctor = QPushButton("Login as Doctor")
        btn_patient = QPushButton("Login as Patient")
        btn_hospital_mgmt = QPushButton("Hospital Management")  # Assuming you kept this

        btn_doctor.setFixedSize(180, 50)
        btn_patient.setFixedSize(180, 50)
        btn_hospital_mgmt.setFixedSize(180, 50)

        btn_doctor.clicked.connect(lambda: self.set_page("doctor_login"))
        btn_patient.clicked.connect(lambda: self.set_page("patient_login"))
        btn_hospital_mgmt.clicked.connect(lambda: self.set_page("admin_login"))

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(btn_doctor)
        h_layout.addWidget(btn_patient)
        h_layout.addWidget(btn_hospital_mgmt)
        h_layout.addStretch()

        layout.addLayout(h_layout)
        layout.addStretch()

        # Add Exit button at bottom right
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()  # Push button to right

        btn_exit = QPushButton("Exit")
        btn_exit.setFixedSize(100, 40)
        btn_exit.clicked.connect(self.close)  # Quit the application
        bottom_layout.addWidget(btn_exit)

        layout.addLayout(bottom_layout)

        self.pages["role_selection"] = page

    # --- admin Page ---
    def init_admin_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_widget.setFixedWidth(300)

        label = QLabel("Hospital Management Login")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: #fff; margin-bottom: 15px;")
        form_layout.addWidget(label)

        self.admin_password_input = QLineEdit()
        self.admin_password_input.setPlaceholderText("Enter Admin Password")
        self.admin_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.admin_password_input.setFixedHeight(40)
        self.admin_password_input.setStyleSheet("""
            background-color: #222;
            color: #fff;
            border-radius: 6px;
            border: 1px solid #666;
            padding-left: 10px;
            font-size: 15px;
        """)
        form_layout.addWidget(self.admin_password_input)

        btn_login = QPushButton("Log in")
        btn_login.clicked.connect(self.admin_login_clicked)
        btn_login.setFixedHeight(40)
        btn_login.setStyleSheet("""
            background-color: #454545;  /* Dark gray */
            color: #fff;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        """)
        form_layout.addWidget(btn_login)

        layout.addWidget(form_widget)
        layout.addStretch()

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.set_page("role_selection"))
        btn_back.setFixedHeight(32)
        btn_back.setFixedWidth(300)
        btn_back.setStyleSheet("""
            background-color: #232323;
            color: #ddd;
            border-radius: 6px;
            margin-top: 8px;
        """)
        layout.addWidget(btn_back)

        self.pages["admin_login"] = page

    def admin_login_clicked(self):
        password = self.admin_password_input.text().strip()
        if password == "adminpass1234":  # Hardcoded admin password
            self.admin_password_input.clear()
            self.set_page("admin_management")
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect admin password.")

    def init_admin_management_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Hospital Management")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        btn_add_patient = QPushButton("Add New Patient")
        btn_add_doctor = QPushButton("Add New Doctor")
        btn_view_patients = QPushButton("View All Patients")  # New button
        btn_view_doctors = QPushButton("View All Doctors")  # New button

        btn_add_patient.setFixedSize(180, 50)
        btn_add_doctor.setFixedSize(180, 50)
        btn_view_patients.setFixedSize(180, 50)
        btn_view_doctors.setFixedSize(180, 50)

        # Connect buttons to respective pages or handlers
        btn_add_patient.clicked.connect(lambda: self.set_page("new_patient"))
        btn_add_doctor.clicked.connect(lambda: self.set_page("new_doctor"))
        btn_view_patients.clicked.connect(lambda: self.load_all_patients())
        btn_view_doctors.clicked.connect(lambda: self.load_all_doctors())

        # Layout for the first two buttons
        h_layout1 = QHBoxLayout()
        h_layout1.addStretch()
        h_layout1.addWidget(btn_add_patient)
        h_layout1.addWidget(btn_add_doctor)
        h_layout1.addStretch()

        # Layout for the new view buttons
        h_layout2 = QHBoxLayout()
        h_layout2.addStretch()
        h_layout2.addWidget(btn_view_patients)
        h_layout2.addWidget(btn_view_doctors)
        h_layout2.addStretch()

        layout.addLayout(h_layout1)
        layout.addLayout(h_layout2)

        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(lambda: self.set_page("role_selection"))
        layout.addWidget(btn_logout)

        layout.addStretch()

        self.pages["admin_management"] = page

    def init_all_doctors_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header_layout = QHBoxLayout()
        title = QLabel("All Doctors")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.set_page("admin_management"))
        header_layout.addWidget(btn_back)

        layout.addLayout(header_layout)

        self.all_doctors_table = QTableWidget()
        self.all_doctors_table.setColumnCount(4)
        self.all_doctors_table.setHorizontalHeaderLabels(["Doctor ID", "Name", "Field", "Experience"])
        self.all_doctors_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.all_doctors_table)

        self.pages["all_doctors"] = page

    def init_all_patients_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header_layout = QHBoxLayout()
        title = QLabel("All Patients")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.set_page("admin_management"))
        header_layout.addWidget(btn_back)

        layout.addLayout(header_layout)

        self.all_patients_table = QTableWidget()
        self.all_patients_table.setColumnCount(5)
        self.all_patients_table.setHorizontalHeaderLabels(["Patient ID", "Name", "Doctor ID", "Age", "Gender"])
        self.all_patients_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.all_patients_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Connect double-click event to handler
        self.all_patients_table.cellDoubleClicked.connect(self.admin_patient_row_clicked)

        layout.addWidget(self.all_patients_table)

        self.pages["all_patients"] = page

    def load_admin_patient_detail_page(self, patient):
        # Compose info including phone number
        info = (
            f"Patient: {patient.get('PatientName', 'Unknown')} | "
            f"ID: {patient.get('PSRN', '')} | "
            f"Phone: {patient.get('PhoneNo', 'N/A')}"
        )
        self.patient_info_label.setText(info)

        password = patient.get('PatientPassword', 'N/A')
        self.patient_password_label.setText(f"Password: {password}")

        records = list(db['Patient_History'].find({"PSRN": patient['PSRN']}, {'_id': 0}).sort("Date and Time", -1))

        self.history_table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.history_table.setItem(row, 0, QTableWidgetItem(record.get("Date and Time", "")))
            self.history_table.setItem(row, 1, QTableWidgetItem(record.get("Remarks", "")))
            self.history_table.setItem(row, 2, QTableWidgetItem(record.get("Medicine Assigned", "")))

        self.remarks_input.clear()
        self.medicine_input.clear()
        self.remarks_input.setEnabled(False)
        self.medicine_input.setEnabled(False)
        self.btn_add_record.setEnabled(False)


    def admin_patient_row_clicked(self, row, column):
        patient_id = self.all_patients_table.item(row, 0).text()
        patient = db['Patient_Info'].find_one({"PSRN": patient_id}, {'_id': 0})
        if not patient:
            QMessageBox.warning(self, "Error", "Patient record not found.")
            return

        self.selected_patient = patient
        self.patient_detail_origin = "admin"
        self.load_admin_patient_detail_page(patient)
        self.set_page("patient_detail")

    # ------- Doctor Login Page -------
    def init_doctor_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Container to center form elements & control width
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_widget.setFixedWidth(300)  # About like Instagram's input width

        self.doctor_id_input = QLineEdit()
        self.doctor_id_input.setPlaceholderText("Doctor ID (e.g. SIHD01)")
        self.doctor_id_input.setFixedHeight(40)
        self.doctor_id_input.setStyleSheet("""
            background-color: #222;
            color: #fff;
            border-radius: 6px;
            border: 1px solid #666;
            padding-left: 10px;
            font-size: 15px;
        """)

        self.doctor_password_input = QLineEdit()
        self.doctor_password_input.setPlaceholderText("Password")
        self.doctor_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.doctor_password_input.setFixedHeight(40)
        self.doctor_password_input.setStyleSheet("""
            background-color: #222;
            color: #fff;
            border-radius: 6px;
            border: 1px solid #666;
            padding-left: 10px;
            font-size: 15px;
        """)

        btn_login = QPushButton("Log in")
        btn_login.clicked.connect(self.doctor_login_clicked)
        btn_login.setFixedHeight(40)
        btn_login.setStyleSheet("""
            background-color: #454545;  /* Not blue */
            color: #fff;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        """)

        form_layout.addWidget(self.doctor_id_input)
        form_layout.addWidget(self.doctor_password_input)
        form_layout.addWidget(btn_login)

        layout.addWidget(form_widget)
        layout.addStretch()

        # Add a back button below (centered)
        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.set_page("role_selection"))
        btn_back.setFixedHeight(32)
        btn_back.setFixedWidth(300)
        btn_back.setStyleSheet("""
            background-color: #232323;
            color: #ddd;
            border-radius: 6px;
            margin-top: 8px;
        """)
        layout.addWidget(btn_back)

        self.pages["doctor_login"] = page

    def doctor_login_clicked(self):
        doc_id = self.doctor_id_input.text().strip()
        password = self.doctor_password_input.text().strip()
        doctor = db['Doctor_Info'].find_one({"SRN": doc_id, "DoctorPass": password})
        if not doctor:
            QMessageBox.warning(self, "Login Failed", "Invalid user credentials")
            return
        self.logged_in_doctor = doctor
        self.load_doctor_dashboard()
        self.set_page("doctor_dashboard")

    # ------- Patient Login Page -------
    def init_patient_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_widget.setFixedWidth(300)

        label = QLabel("Patient Login")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: #fff; margin-bottom: 15px;")
        form_layout.addWidget(label)

        self.patient_phone_input = QLineEdit()
        self.patient_phone_input.setPlaceholderText("Phone Number")
        self.patient_phone_input.setFixedHeight(40)
        self.patient_phone_input.setStyleSheet("""
            background-color: #222;
            color: #fff;
            border-radius: 6px;
            border: 1px solid #666;
            padding-left: 10px;
            font-size: 15px;
        """)
        form_layout.addWidget(self.patient_phone_input)

        self.patient_password_input = QLineEdit()
        self.patient_password_input.setPlaceholderText("Password")
        self.patient_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.patient_password_input.setFixedHeight(40)
        self.patient_password_input.setStyleSheet("""
            background-color: #222;
            color: #fff;
            border-radius: 6px;
            border: 1px solid #666;
            padding-left: 10px;
            font-size: 15px;
        """)
        form_layout.addWidget(self.patient_password_input)

        btn_login = QPushButton("Log in")
        btn_login.clicked.connect(self.patient_login_clicked)
        btn_login.setFixedHeight(40)
        btn_login.setStyleSheet("""
            background-color: #454545;  /* Dark gray */
            color: #fff;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            margin-top: 10px;
        """)
        form_layout.addWidget(btn_login)

        layout.addWidget(form_widget)
        layout.addStretch()

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.set_page("role_selection"))
        btn_back.setFixedHeight(32)
        btn_back.setFixedWidth(300)
        btn_back.setStyleSheet("""
            background-color: #232323;
            color: #ddd;
            border-radius: 6px;
            margin-top: 8px;
        """)
        layout.addWidget(btn_back)

        self.pages["patient_login"] = page

    def patient_login_clicked(self):
        phone = self.patient_phone_input.text().strip()
        password = self.patient_password_input.text().strip()
        patient = db['Patient_Info'].find_one({"PhoneNo": phone, "PatientPassword": password})
        if not patient:
            QMessageBox.warning(self, "Login Failed", "Invalid phone number or password.")
            return
        self.logged_in_patient = patient
        self.load_patient_dashboard()
        self.set_page("patient_dashboard")

    # --- New Doctor Registration Page ---
    def init_new_doctor_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("New Doctor Registration")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.nd_name_input = QLineEdit()
        self.nd_name_input.setPlaceholderText("Doctor Name")
        layout.addWidget(self.nd_name_input)

        self.nd_field_input = QLineEdit()
        self.nd_field_input.setPlaceholderText("Specialization / Field")
        layout.addWidget(self.nd_field_input)

        self.nd_experience_input = QLineEdit()
        self.nd_experience_input.setPlaceholderText("Experience (years)")
        layout.addWidget(self.nd_experience_input)

        self.nd_password_input = QLineEdit()
        self.nd_password_input.setPlaceholderText("Password")
        self.nd_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.nd_password_input)

        btn_add = QPushButton("Add Doctor")
        btn_add.clicked.connect(self.add_new_doctor_record)
        layout.addWidget(btn_add)

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.set_page("admin_management"))  # back to admin page
        layout.addWidget(btn_back)

        layout.addStretch()
        self.pages["new_doctor"] = page

    def add_new_doctor_record(self):
        doctor_info = db['Doctor_Info']

        name = self.nd_name_input.text().strip()
        field = self.nd_field_input.text().strip()
        experience_text = self.nd_experience_input.text().strip()
        password = self.nd_password_input.text().strip()

        if not (name and field and experience_text and password):
            QMessageBox.warning(self, "Input Error", "Please fill all required fields.")
            return

        try:
            experience = int(experience_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Experience must be a valid number.")
            return

        last_doctor = doctor_info.find_one(sort=[('SRN', -1)])
        if last_doctor:
            last_number = int(last_doctor['SRN'][4:])
            new_number = last_number + 1
        else:
            new_number = 1
        SRN = f"SIHD{new_number:02d}"

        doctor = {
            "SRN": SRN,
            "DoctorName": name,
            "DoctorField": field,
            "Experience": experience,
            "DoctorPass": password
        }

        try:
            doctor_info.insert_one(doctor)
            QMessageBox.information(self, "Success", f"Doctor record {SRN} added successfully.")
            self.set_page("admin_management")
            self.nd_name_input.clear()
            self.nd_field_input.clear()
            self.nd_experience_input.clear()
            self.nd_password_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add doctor: {str(e)}")

    # ------- New Patient Registration Page -------
    def init_new_patient_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("New Patient Registration")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.np_name_input = QLineEdit()
        self.np_name_input.setPlaceholderText("Patient Name")
        layout.addWidget(self.np_name_input)

        self.np_age_input = QLineEdit()
        self.np_age_input.setPlaceholderText("Age")
        layout.addWidget(self.np_age_input)

        self.np_gender_input = QLineEdit()
        self.np_gender_input.setPlaceholderText("Gender")
        layout.addWidget(self.np_gender_input)

        self.np_phone_input = QLineEdit()
        self.np_phone_input.setPlaceholderText("Phone Number")
        layout.addWidget(self.np_phone_input)

        self.np_doctor_srn_input = QLineEdit()
        self.np_doctor_srn_input.setPlaceholderText("Doctor Serial Number (e.g. SIHD01)")
        layout.addWidget(self.np_doctor_srn_input)

        btn_add = QPushButton("Add Patient")
        btn_add.clicked.connect(self.add_new_patient_record)
        layout.addWidget(btn_add)

        btn_back = QPushButton("Back")
        btn_back.clicked.connect(lambda: self.set_page("role_selection"))
        layout.addWidget(btn_back)

        layout.addStretch()
        self.pages["new_patient"] = page

    def generate_unique_password(self, collection, field_name="PatientPassword"):
        while True:
            password = str(random.randint(10000, 99999))
            if collection.find_one({field_name: password}) is None:
                return password

    def add_new_patient_record(self):
        patient_info = db['Patient_Info']
        patient_info.create_index('PSRN', unique=True)

        last_patient = patient_info.find_one(sort=[('PSRN', -1)])
        if last_patient:
            last_number = int(last_patient['PSRN'][4:])
            new_number = last_number + 1
        else:
            new_number = 1
        PSRN = f"SIHP{new_number:02d}"

        name = self.np_name_input.text().strip()
        age_text = self.np_age_input.text().strip()
        gender = self.np_gender_input.text().strip()
        phone = self.np_phone_input.text().strip()
        doctor_srn = self.np_doctor_srn_input.text().strip()
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M")

        if not (name and age_text and gender and phone and doctor_srn):
            QMessageBox.warning(self, "Input Error", "Please fill all required fields.")
            return
        try:
            age = int(age_text)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be a valid number.")
            return

        password = self.generate_unique_password(patient_info, "PatientPassword")

        if not doctor_srn.startswith("SIHD"):
            doctor_srn = "SIHD" + doctor_srn

        patient = {
            "PSRN": PSRN,
            "DoctorSRN": doctor_srn,
            "PatientName": name,
            "PatientAge": age,
            "PatientGender": gender,
            "PatientPassword": password,
            "PhoneNo": phone,
            "Date and Time": current_time
            # Remove PatientRemarks and PatientMedicine keys
        }

        try:
            patient_info.insert_one(patient)
            QMessageBox.information(self, "Success",
                                    f"Patient record {PSRN} added with password {password}.")
            self.set_page("role_selection")
            self.np_name_input.clear()
            self.np_age_input.clear()
            self.np_gender_input.clear()
            self.np_phone_input.clear()
            self.np_doctor_srn_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add patient record: {str(e)}")

    # ------- Doctor Dashboard -------
    def init_doctor_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header_layout = QHBoxLayout()
        self.doctor_info_label = QLabel()
        self.doctor_info_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        header_layout.addWidget(self.doctor_info_label)
        header_layout.addStretch()

        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        header_layout.addWidget(btn_logout)

        layout.addLayout(header_layout)

        # Updated doctor dashboard columns without remarks, medicine, date/time
        self.patient_table = QTableWidget()
        self.patient_table.setColumnCount(5)
        self.patient_table.setHorizontalHeaderLabels([
            "Patient ID", "Patient Name", "Phone No.", "Age", "Gender"
        ])
        self.patient_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.patient_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.patient_table.cellDoubleClicked.connect(self.patient_row_clicked)
        layout.addWidget(self.patient_table)

        self.pages["doctor_dashboard"] = page

    def load_doctor_dashboard(self):
        doctor = self.logged_in_doctor
        text = f"Dr. {doctor.get('DoctorName', 'Unknown')} | Field: {doctor.get('DoctorField', 'N/A')} | Experience: {doctor.get('Experience', 'N/A')}"
        self.doctor_info_label.setText(text)

        patients = list(db['Patient_Info'].find({"DoctorSRN": doctor['SRN']}, {'_id': 0}))
        self.patient_table.setRowCount(len(patients))
        for row, patient in enumerate(patients):
            self.patient_table.setItem(row, 0, QTableWidgetItem(patient.get('PSRN', '')))
            self.patient_table.setItem(row, 1, QTableWidgetItem(patient.get('PatientName', '')))
            self.patient_table.setItem(row, 2, QTableWidgetItem(patient.get('PhoneNo', '')))
            self.patient_table.setItem(row, 3, QTableWidgetItem(str(patient.get('PatientAge', ''))))
            self.patient_table.setItem(row, 4, QTableWidgetItem(patient.get('PatientGender', '')))

    # ------- Patient Row Clicked (missing method added) -------
    def patient_row_clicked(self, row, column):
        patient_id = self.patient_table.item(row, 0).text()
        patient = db['Patient_Info'].find_one({"PSRN": patient_id}, {'_id': 0})
        if not patient:
            QMessageBox.warning(self, "Error", "Patient record not found.")
            return

        self.selected_patient = patient
        self.patient_detail_origin = "doctor"  # Set origin as doctor
        self.load_patient_detail_page(patient)
        self.set_page("patient_detail")

    # ------- Patient Detail Page -------
    def init_patient_detail_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header_layout = QHBoxLayout()

        self.patient_info_label = QLabel()
        self.patient_info_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        header_layout.addWidget(self.patient_info_label)

        # Label to show patient password (shown only to admin)
        self.patient_password_label = QLabel()
        self.patient_password_label.setStyleSheet(
            "font-weight: normal; font-size: 14px; color: #888; margin-left: 15px;")
        header_layout.addWidget(self.patient_password_label)

        header_layout.addStretch()

        btn_back = QPushButton("Back")

        def handle_back():
            if self.patient_detail_origin == "admin":
                self.set_page("admin_management")
            else:
                self.set_page("doctor_dashboard")

        btn_back.clicked.connect(handle_back)
        header_layout.addWidget(btn_back)

        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        header_layout.addWidget(btn_logout)

        layout.addLayout(header_layout)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels([
            "Date and Time", "Remarks", "Medicine Assigned"
        ])
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addWidget(self.history_table)

        add_layout = QHBoxLayout()
        self.remarks_input = QLineEdit()
        self.remarks_input.setPlaceholderText("Enter Remarks")
        add_layout.addWidget(self.remarks_input)

        self.medicine_input = QLineEdit()
        self.medicine_input.setPlaceholderText("Enter Medicine")
        add_layout.addWidget(self.medicine_input)

        self.btn_add_record = QPushButton("Add Record")
        self.btn_add_record.clicked.connect(self.add_history_record)
        add_layout.addWidget(self.btn_add_record)

        layout.addLayout(add_layout)

        self.pages["patient_detail"] = page

    def load_patient_detail_page(self, patient):
        info = f"Patient: {patient.get('PatientName', 'Unknown')} | ID: {patient.get('PSRN', '')}"
        self.patient_info_label.setText(info)

        self.patient_password_label.setText("")  # Hide password for doctors

        records = list(db['Patient_History'].find({"PSRN": patient['PSRN']}, {'_id': 0}).sort("Date and Time", -1))

        self.history_table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.history_table.setItem(row, 0, QTableWidgetItem(record.get("Date and Time", "")))
            self.history_table.setItem(row, 1, QTableWidgetItem(record.get("Remarks", "")))
            self.history_table.setItem(row, 2, QTableWidgetItem(record.get("Medicine Assigned", "")))

        self.remarks_input.setEnabled(True)
        self.medicine_input.setEnabled(True)
        self.btn_add_record.setEnabled(True)

        # Ensure Add Record button is connected only in doctor view
        try:
            self.btn_add_record.clicked.disconnect()
        except TypeError:
            pass
        self.btn_add_record.clicked.connect(self.add_history_record)

    def add_history_record(self):
        remarks = self.remarks_input.text().strip()
        medicine = self.medicine_input.text().strip()

        if not remarks or not medicine:
            QMessageBox.warning(self, "Input Error", "Remarks and Medicine cannot be empty.")
            return

        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_record = {
            "PSRN": self.selected_patient['PSRN'],
            "Date and Time": dt,
            "Remarks": remarks,
            "Medicine Assigned": medicine
        }

        try:
            db['Patient_History'].insert_one(new_record)
            QMessageBox.information(self, "Success", "Record added to history.")
            self.load_patient_detail_page(self.selected_patient)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add record: {str(e)}")

    # ------- Patient Dashboard -------
    def init_patient_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        header_layout = QHBoxLayout()

        self.patient_dashboard_info_label = QLabel()
        self.patient_dashboard_info_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        header_layout.addWidget(self.patient_dashboard_info_label)

        header_layout.addStretch()

        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        header_layout.addWidget(btn_logout)

        layout.addLayout(header_layout)

        self.patient_history_table = QTableWidget()
        self.patient_history_table.setColumnCount(3)
        self.patient_history_table.setHorizontalHeaderLabels([
            "Date and Time", "Remarks", "Medicine Assigned"
        ])
        self.patient_history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.patient_history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addWidget(self.patient_history_table)

        self.pages["patient_dashboard"] = page

    def load_patient_dashboard(self):
        patient = self.logged_in_patient
        info = f"Patient: {patient.get('PatientName', 'Unknown')} | ID: {patient.get('PSRN', '')}"
        self.patient_dashboard_info_label.setText(info)

        records = list(db['Patient_History'].find({"PSRN": patient['PSRN']}, {'_id': 0}).sort("Date and Time", -1))
        self.patient_history_table.setRowCount(len(records))
        for row, record in enumerate(records):
            self.patient_history_table.setItem(row, 0, QTableWidgetItem(record.get("Date and Time", "")))
            self.patient_history_table.setItem(row, 1, QTableWidgetItem(record.get("Remarks", "")))
            self.patient_history_table.setItem(row, 2, QTableWidgetItem(record.get("Medicine Assigned", "")))

    # ------- Logout -------
    def logout(self):
        self.logged_in_doctor = None
        self.logged_in_patient = None
        self.selected_patient = None
        self.doctor_id_input.clear()
        self.doctor_password_input.clear()
        self.patient_phone_input.clear()
        self.patient_password_input.clear()
        self.set_page("role_selection")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HospitalApp()
    window.show()
    sys.exit(app.exec())

