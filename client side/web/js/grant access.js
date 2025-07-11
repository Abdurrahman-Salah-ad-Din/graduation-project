document.addEventListener("DOMContentLoaded", () => {
    // Check authentication first
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
        alert("No access token found. Please login.");
        window.location.href = 'login.html';
        return;
    }

    // Logout functionality (matches your reference code exactly)
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.clear();
            window.location.href = 'login.html';
        });
    }

    // Grant Access form submission
    const grantAccessBtn = document.getElementById('grant-access-btn');
    if (grantAccessBtn) {
        grantAccessBtn.addEventListener('click', async function() {
            try {
                // Get form values
                const patientId = document.getElementById('patient-id').value.trim();
                const staffId = document.getElementById('staff-id').value.trim();
                const accessLevel = document.getElementById('access-level').value;

                // Validate inputs
                if (!patientId) {
                    throw new Error('Patient ID Code is required');
                }

                // Prepare the request payload
                const payload = {
                    patient_id: patientId,
                    access_level: accessLevel
                };

                // Add staff_id only if provided
                if (staffId) {
                    payload.staff_id = staffId;
                }

                // Make API request
                const response = await fetch('http://localhost:8000/patients/grant-access', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                // Handle response
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Failed to grant access');
                }

                // Success case
                const result = await response.json();
                console.log("Access granted successfully:", result);
                
                alert(`Access granted successfully for patient ${patientId}`);
                
                // Reset form
                document.getElementById('patient-id').value = '';
                document.getElementById('staff-id').value = '';
                document.getElementById('access-level').value = 'view';

            } catch (error) {
                console.error('Error granting access:', error);
                alert(`Error: ${error.message}`);
            }
        });
    }
});