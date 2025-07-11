document.addEventListener('DOMContentLoaded', function() {
    const accessToken = localStorage.getItem('access_token');
    const patientList = document.getElementById('radiologistList');
    
    // Debugging
    console.log('Access Token:', accessToken);
    console.log('radiologist List Element:', patientList);

    // Check authentication
    if (!accessToken) {
        console.error('No access token found, redirecting to login');
        window.location.href = 'login.html';
        return;
    }

    // Load radiologists
    async function loadRadiologists() {
        try {
            console.log('Starting to load radiologist...');
            radiologistList.innerHTML = '<div class="loading">Loading radiologists...</div>';
            
            const response = await fetch('http://localhost:8000/users/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            });

            console.log('API Response Status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('API Error Response:', errorText);
                throw new Error(`Server responded with status ${response.status}`);
            }

            const data = await response.json();
            console.log('API Data Received:', data);
            
            // Handle different response formats
            let radiologists = [];
            if (Array.isArray(data)) {
                radiologists = data;
            } else if (data && typeof data === 'object') {
                radiologists = data.radiologists || data.data || data.results || [];
            }

            console.log('Processed radiologists:', radiologists);
            
            if (!Array.isArray(radiologists)) {
                throw new Error('Invalid radiologists data format - expected array');
            }

            displayRadiologists(radiologists);
        } catch (error) {
            console.error('Error in loadradiologists:', error);
            patientList.innerHTML = `<div class="error">Error loading radiologists: ${error.message}</div>`;
        }
    }

    // Display radiologists
    function displayRadiologists(radiologists) {
        console.log('Displaying radiologists:', radiologists);
        
        if (!radiologists || radiologists.length === 0) {
            radiologistList.innerHTML = '<div class="no-radiologists">No radiologists found</div>';
            return;
        }

        radiologistList.innerHTML = radiologists.map(radiologist => {
            // Debug each radiologist object
            console.log('Processing radiologist:', radiologist);
            
            const id = radiologist.id || radiologist._id || 'unknown';
            const firstName = radiologist.first_name || radiologist.firstName || 'Unknown';
            const lastName = radiologist.last_name || radiologist.lastName || '';
            const email = radiologist.email || 'No email provided';
            const phone = radiologist.phone_number || radiologist.phone || 'No phone provided';
            
            return `
                <div class="radiologist-entry" data-id="${id}">
                    <div>
                        <strong>${firstName} ${lastName}</strong><br>
                        ${email}<br>
                        Phone: ${phone}
                    </div>
                    <a href="#" class="delete-link" data-id="${id}">Delete</a>
                </div>
            `;
        }).join('');

        // Add event listeners to delete buttons
        document.querySelectorAll('.delete-link').forEach(link => {
            link.addEventListener('click', async function(e) {
                e.preventDefault();
                const radiologistId = this.getAttribute('data-id');
                const radiologistName = this.closest('.radiologist-entry').querySelector('strong').textContent;
                
                if (confirm(`Are you sure you want to delete ${radiologistName}?`)) {
                    await deletePatient(radiologistId);
                }
            });
        });
    }

    // Delete radiologist
    async function deletePatient(radiologistId) {
        try {
            console.log('Attempting to delete radiologist ID:', radiologistId);
            const response = await fetch(`http://localhost:8000/users/${radiologistId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            });

            console.log('Delete response status:', response.status);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Delete error response:', errorData);
                throw new Error(errorData.message || 'Failed to delete radiologist');
            }

            // Remove the radiologist from the UI
            const radiologistElement = document.querySelector(`.radiologist-entry[data-id="${radiologistId}"]`);
            if (radiologistElement) {
                radiologistElement.remove();
                console.log('radiologist removed from UI');
            }
            
            // Show success message
            const successMsg = document.createElement('div');
            successMsg.className = 'success';
            successMsg.textContent = 'radiologist deleted successfully';
            patientList.prepend(successMsg);
            setTimeout(() => successMsg.remove(), 3000);

            // Reload if no radiologists left
            if (document.querySelectorAll('.radiologist-entry').length === 0) {
                radiologistList.innerHTML = '<div class="no-radiologists">No radiologists found</div>';
            }
        } catch (error) {
            console.error('Error in deleteRadiologist:', error);
            alert(`Error deleting radiologist: ${error.message}`);
        }
    }

    // Logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.clear();
            window.location.href = 'login.html';
        });
    }

    // Initial load
    loadRadiologists();
});