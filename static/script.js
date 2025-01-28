function fetchPatient() {
    let patientId = document.getElementById("patientId").value;
    let errorMessage = document.getElementById("errorMessage");
    let patientInfo = document.getElementById("patientInfo");

    // Clear previous messages
    errorMessage.textContent = "";
    patientInfo.style.display = "none";
    patientInfo.innerHTML = "";

    if (!patientId) {
        errorMessage.textContent = "Please enter a valid Patient ID.";
        return;
    }

    fetch(`/patients/${patientId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Patient not found.");
            }
            return response.json();
        })
        .then(data => {
            let patient = data.data;
            patientInfo.innerHTML = `
                <h3 style="text-align:center; margin-bottom:10px;">Patient Details</h3>
                <table class="patient-info-table">
                    <tr><td>Name:</td><td>${patient.name}</td></tr>
                    <tr><td>Age:</td><td>${patient.age}</td></tr>
                    <tr><td>Gender:</td><td>${patient.gender}</td></tr>
                    <tr><td>Contact:</td><td>${patient.contact}</td></tr>
                    <tr><td>Address:</td><td>${patient.address}</td></tr>
                    <tr><td>Medical History:</td><td>${patient.medical_history.join(", ")}</td></tr>
                    <tr><td>Assigned Doctor:</td><td>${patient.assigned_doctor}</td></tr>
                </table>
            `;
            patientInfo.style.display = "block";
        })
        .catch(error => {
            errorMessage.textContent = error.message;
        });
}
