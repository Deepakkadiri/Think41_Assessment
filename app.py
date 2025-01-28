from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime, timedelta
import logging

# Set up logging configuration
logging.basicConfig(filename='prescription_audit.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enables CORS for frontend requests

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  # Change if needed
db = client["hospital_db"]
patients_collection = db["patients"]  # Patient records
doctors_collection = db["doctors"]  # Doctor records
prescriptions_collection = db["prescriptions"]  # Prescription records

@app.route("/")
def homepage():
    return render_template("index2.html")


# Serve the prescription page
@app.route("/prescribe", methods=["GET"])
def prescribe_page():
    return render_template("prescribe.html")

# Function to check if the prescription is within a valid time window (24 hours)

def is_prescription_valid(prescription_time):
    """Checks if the prescription is issued within a valid time frame."""
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")  # Extract current timestamp directly as a string
    current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")  # Convert back to datetime object
    
    prescription_datetime = datetime.strptime(prescription_time, "%Y-%m-%d %H:%M:%S")  # Convert string to datetime

    # Time window: prescriptions should be issued within 24 hours
    return (current_time - prescription_datetime) <= timedelta(hours=24)

# Function to log prescription details for audit trail
def log_prescription(prescription_data, status):
    log_message = f"Prescription for Patient {prescription_data['patient_id']} " \
                  f"by Doctor {prescription_data['doctor_id']} " \
                  f"Medications: {prescription_data['medication']} " \
                  f"Status: {status}"
    logging.info(log_message)

# API to prescribe medication for a patient
@app.route("/prescribe", methods=["POST"])
def prescribe():
    """Allow a doctor to prescribe medication to a patient."""
    data = request.get_json()

    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    medication = data.get("medication")
    dose = data.get("dose")
    prescription_time = data.get("date", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))  # Default to current time

    # Check if prescription time is valid
    if not is_prescription_valid(prescription_time):
        log_prescription(data, "Invalid - Time expired")
        return jsonify({"status": "error", "message": "Prescription time window has expired."}), 400

    # Validate doctor-patient relationship
    patient = patients_collection.find_one({"_id": patient_id})
    if not patient:
        log_prescription(data, "Invalid - Patient not found")
        return jsonify({"status": "error", "message": "Patient not found."}), 404
    
    # Compare the assigned_doctor field (string) with the doctor_id
    if patient.get("assigned_doctor") != doctor_id:
        log_prescription(data, "Invalid - Unauthorized doctor")
        return jsonify({"status": "error", "message": "You are not authorized to prescribe for this patient."}), 403

    # Create prescription record
    prescription = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "medication": medication,
        "dose": dose,
        "date": prescription_time
    }
    prescriptions_collection.insert_one(prescription)

    # Log the successful prescription
    log_prescription(data, "Success")
    return jsonify({"status": "success", "message": "Prescription added successfully."}), 201

# API to fetch patient details by ID
@app.route("/patients/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    """Fetch patient details by ID"""
    patient = patients_collection.find_one({"_id": patient_id})
    
    if patient:
        # Convert MongoDB ObjectId to string if needed
        patient["_id"] = str(patient["_id"])
        return jsonify({"status": "success", "data": patient}), 200
    else:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

# API to add a new doctor
@app.route("/doctors", methods=["POST"])
def add_doctor():
    """Add a new doctor to the system."""
    data = request.get_json()

    doctor_id = data.get("doctor_id")
    name = data.get("name")
    specialization = data.get("specialization")
    contact = data.get("contact")
    
    if not doctor_id or not name or not specialization or not contact:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    # Check if the doctor already exists
    existing_doctor = doctors_collection.find_one({"doctor_id": doctor_id})
    if existing_doctor:
        return jsonify({"status": "error", "message": "Doctor already exists."}), 409
    
    doctor = {
        "doctor_id": doctor_id,
        "name": name,
        "specialization": specialization,
        "contact": contact
    }

    doctors_collection.insert_one(doctor)
    return jsonify({"status": "success", "message": "Doctor added successfully."}), 201






@app.route("/update_prescription_form")
def update_prescription_form():
    """Route to serve the Update Prescription page."""
    return render_template("update_prescribe.html")


@app.route("/update_prescription", methods=["PUT"])
def update_prescription():
    """API to update an existing prescription."""
    data = request.json
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    new_medication = data.get("medication")
    new_dose = data.get("dose")
    new_prescription_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")  # Auto-fill current time

    # Find the patient
    patient = patients_collection.find_one({"_id": patient_id})
    if not patient:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

    # Ensure doctor is assigned to the patient
    if patient["assigned_doctor"] != doctor_id:
        return jsonify({"status": "error", "message": "Doctor is not assigned to this patient"}), 403

    # Find latest prescription
    latest_prescription = prescriptions_collection.find_one({"patient_id": patient_id}, sort=[("date", -1)])
    if not latest_prescription:
        return jsonify({"status": "error", "message": "No prescription found for this patient"}), 404

    # Validate time window
    if not is_prescription_valid(latest_prescription["date"]):
        return jsonify({"status": "error", "message": "Prescription update period expired"}), 403

    # Update the prescription
    prescriptions_collection.update_one(
        {"_id": latest_prescription["_id"]},
        {"$set": {"medication": new_medication, "dose": new_dose, "date": new_prescription_time}}
    )

    return jsonify({"status": "success", "message": "Prescription updated successfully"}), 200



@app.route("/delete_prescription_form")
def delete_prescription_form():
    """Route to serve the Delete Prescription page."""
    return render_template("delete_prescribe.html")


@app.route("/delete_prescription", methods=["DELETE"])
def delete_prescription():
    """API to delete an existing prescription."""
    data = request.json
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")

    # Find the patient
    patient = patients_collection.find_one({"_id": patient_id})
    if not patient:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

    # Ensure doctor is assigned to the patient
    if patient["assigned_doctor"] != doctor_id:
        return jsonify({"status": "error", "message": "Doctor is not assigned to this patient"}), 403

    # Find latest prescription
    latest_prescription = prescriptions_collection.find_one({"patient_id": patient_id}, sort=[("date", -1)])
    if not latest_prescription:
        return jsonify({"status": "error", "message": "No prescription found for this patient"}), 404

    # Delete the prescription
    prescriptions_collection.delete_one({"_id": latest_prescription["_id"]})

    return jsonify({"status": "success", "message": "Prescription deleted successfully"}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
