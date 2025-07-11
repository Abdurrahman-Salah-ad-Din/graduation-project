function select_filter(x) {
    // Set the active class for the selected filter
    let activeFilter = document.getElementById(`filter${x}`);
    activeFilter.className = "time-filter active";

    // Remove the active class from the other filters
    for (let i = 1; i <= 4; i++) {
        if (i !== x) {
            document.getElementById(`filter${i}`).className = "time-filter";
        }
    }
}

const accessToken = localStorage.getItem('access_token');
const refreshToken = localStorage.getItem('refresh_token');
const userData = JSON.parse(localStorage.getItem('user'));

document.addEventListener('DOMContentLoaded', async function() {
    document.getElementById('logout-btn').addEventListener('click', async () => {
        try {
            const response = await fetch('http://localhost:8000/users/logout/', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + accessToken,
                    'Content-Type': 'application/json'
                }
            });
            
            localStorage.clear();
            window.location.href = 'login.html';
        } catch (error) {
            console.error('Logout failed:', error);
        }

    if (!userData) {
        // If no user data, redirect back to login
        window.location.href = "login.html";
        return;
    }});

    try {
        const response = await fetch('http://localhost:8000/patients/', {
            method: 'GET',
            headers: {
                'Content-Type': "application/json",
                'Authorization': 'Bearer ' + accessToken
            }
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.errors || 'failed');
        }

        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('user', JSON.stringify(userData));
        console.log('Access Token : ',accessToken)

        const data = await response.json();
        const patients = data.data;
        const patients_num = data.data.length;
        document.getElementById("patients_num").innerHTML = patients_num;
        
        let cases_num = 0
        for (let i = 0; i < patients_num; i++) {
            cases_num += data.data[i].scans.length;
        }

        document.getElementById("cases_num").innerHTML = cases_num; 
        document.querySelectorAll('.patient-name').length;
        
        // Get the container for patient cards
        const patientsGrid = document.querySelector('.patients-grid');
        patientsGrid.innerHTML = ''; // Clear existing cards

        // Determine which patients to show
        const patientsToShow = patients_num < 6 ? patients : patients.slice(-6);

        // Create and append patient cards
        patientsToShow.forEach(patient => {
            // Skip if no scans
            if (!patient.scans || patient.scans.length === 0) return;
            
            const latestScan = patient.scans[0];
            
            // Skip if scan is missing required data
            if (!latestScan || !latestScan.created_at || !latestScan.image_scan_url) {
                console.warn(`Skipping patient ${patient.id} - incomplete scan data`);
                return;
            }
        
            const card = document.createElement('div');
            card.className = 'patient-card';
            
            // Add click event to redirect to view patient.html with patient ID
            card.addEventListener('click', () => {
                window.location.href = `view patient.html?id=${patient.id}`;
            });
            
            const scanDate = new Date(latestScan.created_at);
            const formattedDate = scanDate.toLocaleDateString('en-CA').replace(/-/g, '/');
            let diagnosis =''
            if (latestScan.predictions?.[0]?.confidence > 0.5 ){
                diagnosis = latestScan.predictions?.[0]?.disease
            }
            else{
                diagnosis = 'Healthy'
            }
            card.innerHTML = `
                <div class="patient-name">${patient.first_name} ${patient.last_name}</div>
                <div class="scan-image-container">
                    <img src="${latestScan.image_scan_url}" alt="Scan for ${patient.first_name}" 
                         class="scan-image"
                         onerror="this.style.display='none'">
                </div>
                <div class="diagnosis-item">
                    <div class="diagnosis-info">
                        <div class="diagnosis-name">
                            ${diagnosis}
                        </div>
                        <div class="diagnosis-category">
                            Chest
                        </div>
                    </div>
                    <div class="diagnosis-date">${formattedDate}</div>
                </div>
            `;
            
            patientsGrid.appendChild(card);
        });
    
    } catch (error) {
        alert(error.message || 'failed. Please try again.'); // Simple error handling
    };
});