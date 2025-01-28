# **Hospital Management System**

## 📌 Overview
The **Hospital Management System** is a web-based application designed to manage patient records, prescriptions, and doctor assignments efficiently. It provides secure API endpoints for adding, updating, deleting, and retrieving patient prescriptions while maintaining proper authorization and data integrity.

---

## 🚀 Features
✅ **Assign Doctor to Patient:** Ensures that only an assigned doctor can prescribe for a patient.  
✅ **Issue Prescription:** Doctors can issue prescriptions with a timestamp, and the system enforces a 24-hour validity window.  
✅ **Update Prescription:** Existing prescriptions can be updated based on patient ID.  
✅ **Delete Prescription:** Only assigned doctors can delete prescriptions, and all deletions are logged for audit purposes.  
✅ **Logging & Auditing:** All prescription deletions are logged, including timestamps and user details, for tracking purposes.

---

## 🔗 API Endpoints
### 📍 1. Fetch Patient Details
- **Endpoint:** `GET /patients/<patient_id>`  
- **Description:** Fetches patient details based on their ID.  

### 📍 2. Add a New Doctor
- **Endpoint:** `POST /add_doctor`  
- **Description:** Adds a new doctor record while ensuring unique doctor IDs.

### 📍 3. Issue Prescription
- **Endpoint:** `POST /issue_prescription`  
- **Description:** Allows an assigned doctor to prescribe medication to a patient, ensuring that the prescription is within a 24-hour validity period.

### 📍 4. Update Prescription
- **Endpoint:** `PUT /update_prescription`  
- **Description:** Updates an existing prescription for a patient.

### 📍 5. Delete Prescription
- **Endpoint:** `DELETE /delete_prescription`  
- **Description:** Allows assigned doctors to delete a prescription for their patient. Unauthorized requests are denied.

---

## 🛠 Data Constraints & Validations
🔹 **Doctor-Patient Relationship:** Only assigned doctors can prescribe or delete prescriptions.  
🔹 **Unique Doctor IDs:** Ensured during doctor registration.  
🔹 **Prescription Validity:** Only prescriptions issued within the last 24 hours are valid.  
🔹 **Deletion Authorization:** Only assigned doctors can delete prescriptions.  

---

## 📜 Logging Mechanism
To maintain an audit trail of deleted prescriptions, a logging system records each deletion attempt. The logs capture:
- **Doctor ID** performing the action
- **Patient ID** associated with the prescription
- **Timestamp** of deletion

### 📝 Example Log Entries:
```bash
2025-01-28 15:30:00 - Doctor D2002 is deleting prescription for Patient P1001.
2025-01-28 15:30:10 - Prescription deleted successfully for Patient P1001 by Doctor D2002.
```

---

## 📖 Setup Instructions
### 🔹 Install Dependencies
```bash
pip install flask pymongo flask-cors
```
### 🔹 Run the Application
```bash
python app.py
```
### 🔹 Access the Application
- Open `http://127.0.0.1:5000/` in a web browser.

---

## 💻 Technologies Used
- **Backend:** Flask (Python)
- **Database:** MongoDB
- **Frontend:** HTML, CSS, JavaScript

---

## 📌 Future Enhancements
🔹 Implement authentication for doctors and admin roles.  
🔹 Add a feature to track prescription history for patients.  
🔹 Provide an analytics dashboard for hospital administrators.  

---

## 📜 License
This project is licensed under the **MIT License**.
