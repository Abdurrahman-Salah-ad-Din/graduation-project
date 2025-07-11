document.addEventListener('DOMContentLoaded', function() {
    const accessToken = localStorage.getItem('access_token');
    const patientList = document.getElementById('patientList');
    const searchInput = document.getElementById('patientSearch');
    const clearButton = document.getElementById('clearSearch');
    let allPatients = [];
    
    // Check authentication
    if (!accessToken) {
        window.location.href = 'login.html';
        return;
    }

    // Filter patients based on search term
    function filterPatients(searchTerm) {
        if (!searchTerm) return allPatients;
        const term = searchTerm.toLowerCase().trim();
        
        return allPatients.filter(patient => {
            const firstName = (patient.first_name || patient.firstName || '').toLowerCase();
            const lastName = (patient.last_name || patient.lastName || '').toLowerCase();
            const fullName = `${firstName} ${lastName}`;
            
            return firstName.startsWith(term) || 
                   lastName.startsWith(term) ||
                   fullName.includes(term);
        });
    }

    // Load patients
    async function loadPatients() {
        try {
            patientList.innerHTML = '<div class="loading">Loading patients...</div>';
            
            const response = await fetch('http://localhost:8000/patients/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }

            const data = await response.json();
            
            // Handle different response formats
            allPatients = Array.isArray(data) ? data : 
                        (data && typeof data === 'object') ? 
                        (data.patients || data.data || data.results || []) : [];

            if (!Array.isArray(allPatients)) {
                throw new Error('Invalid patients data format - expected array');
            }

            displayPatients(allPatients);
        } catch (error) {
            patientList.innerHTML = `<div class="error">Error loading patients: ${error.message}</div>`;
        }
    }

    // Display patients
    function displayPatients(patients) {
        if (!patients || patients.length === 0) {
            patientList.innerHTML = '<div class="no-patients">No patients found</div>';
            return;
        }

        patientList.innerHTML = patients.map(patient => {
            const id = patient.id || 'unknown';
            const firstName = patient.first_name || 'Unknown';
            const lastName = patient.last_name || '';
            const email = patient.email || 'No email provided';
            const code = patient.code || 'No email provided';
            
            return `
                <div class="patient-entry" data-id="${id}">
                    <div class="patient-info">
                        <strong>${firstName} ${lastName}</strong>
                        <br>✉️ ${email} |
                        <br>🔑 ${code}
                    </div>
                    <a href="#" class="add-scan" data-id="${id}">Add scan</a>
                    <a href="#" class="delete-link" data-id="${id}">Delete</a>
                </div>
            `;
        }).join('');

        // Make entire patient entry clickable
        document.querySelectorAll('.patient-entry').forEach(entry => {
            entry.addEventListener('click', function(e) {
                // Don't redirect if clicking on delete or add scan buttons
                if (e.target.classList.contains('delete-link') || 
                    e.target.classList.contains('add-scan')) {
                    return;
                }
                
                const patientId = this.getAttribute('data-id');
                window.location.href = `view patient.html?id=${patientId}`;
            });
        });

        // Delete button functionality
        document.querySelectorAll('.delete-link').forEach(link => {
            link.addEventListener('click', async function(e) {
                e.stopPropagation();
                const patientId = this.getAttribute('data-id');
                const patientName = this.closest('.patient-entry').querySelector('strong').textContent;
                
                if (confirm(`Are you sure you want to delete ${patientName}?`)) {
                    await deletePatient(patientId);
                }
            });
        });
    
        // Add scan button functionality
        document.querySelectorAll('.add-scan').forEach(link => {
            link.addEventListener('click', function(e) {
                e.stopPropagation();
                const patientId = this.getAttribute('data-id');
                window.location.href = `scan.html?patient_id=${patientId}`;
            });
        });
    }
    
    // Delete patient
    async function deletePatient(patientId) {
        try {
            const response = await fetch(`http://localhost:8000/patients/${patientId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || 'Failed to delete patient');
            }

            // Update the allPatients array
            allPatients = allPatients.filter(p => (p.id || p._id) !== patientId);
            
            // Re-filter with current search term
            const filtered = filterPatients(searchInput.value.trim());
            displayPatients(filtered);
            
            // Show success message
            const successMsg = document.createElement('div');
            successMsg.className = 'success';
            successMsg.textContent = 'Patient deleted successfully';
            patientList.prepend(successMsg);
            setTimeout(() => successMsg.remove(), 3000);

        } catch (error) {
            alert(`Error deleting patient: ${error.message}`);
        }
    }

    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.trim();
        const filteredPatients = filterPatients(searchTerm);
        displayPatients(filteredPatients);
    });

    // Clear search
    clearButton.addEventListener('click', function() {
        searchInput.value = '';
        displayPatients(allPatients);
    });

    // Logout functionality
    document.getElementById('logout-btn')?.addEventListener('click', function() {
        localStorage.clear();
        window.location.href = 'login.html';
    });

    // Initial load
    loadPatients();
});