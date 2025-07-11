document.addEventListener("DOMContentLoaded", () => {
    const scanState = {
        currentMainScan: null,
        currentOtherScans: []
    };

    const getElement = (id) => {
        const el = document.getElementById(id);
        if (!el) console.error(`Element with ID ${id} not found`);
        return el;
    };

    const basicInfoElement = getElement('basic-info');
    const mainScanContainer = getElement('main-scan');
    const otherScansContainer = getElement('other-scans');
    const uploadBtn = getElement('upload-btn');
    const fileInput = getElement('fileInput');
    const previewContainer = getElement('preview-container');
    const previewImage = getElement('preview-image');
    const fileInfo = getElement('file-info');
    const submitScanBtn = getElement('submit-scan');
    const organSelect = getElement('organSelect');
    const additionalInfo = getElement('additionalInfo');
    const logoutBtn = getElement('logout-btn');
    const cancelScanBtn = getElement('cancel-scan');

    if (!basicInfoElement || !mainScanContainer || !otherScansContainer) {
        console.error('Essential elements missing from DOM');
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const patientId = urlParams.get('id');

    if (!patientId) {
        alert('Patient ID not found in URL');
        window.location.href = 'patients.html';
        return;
    }

    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
        alert("No access token found. Please login.");
        window.location.href = 'login.html';
        return;
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', function () {
            localStorage.clear();
            window.location.href = 'login.html';
        });
    }

    let selectedFile = null;

    if (uploadBtn && fileInput) {
        uploadBtn.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                selectedFile = this.files[0];
                uploadBtn.textContent = 'Change Scan';

                const reader = new FileReader();
                reader.onload = function (e) {
                    if (previewImage) previewImage.src = e.target.result;
                    if (previewContainer) previewContainer.style.display = 'block';
                    if (fileInfo) fileInfo.textContent = `File: ${selectedFile.name} (${(selectedFile.size / 1024).toFixed(1)} KB)`;
                };
                reader.readAsDataURL(selectedFile);
            }
        });
    }

    if (cancelScanBtn) {
        cancelScanBtn.addEventListener('click', function () {
            fileInput.value = '';
            if (previewContainer) previewContainer.style.display = 'none';
            if (uploadBtn) uploadBtn.textContent = 'Upload Scan';
            selectedFile = null;
            if (additionalInfo) additionalInfo.value = '';
        });
    }

    async function fetchPatientData() {
        try {
            const response = await fetch(`http://localhost:8000/patients/${patientId}/`, {
                headers: {
                    'Authorization': 'Bearer ' + accessToken
                }
            });

            if (!response.ok) throw new Error('Failed to fetch patient');

            const responseData = await response.json();

            const patient = responseData.data;

            displayPatientInfo(patient);

            if (patient.scans && patient.scans.length > 0) {
                displayScans(patient.scans);
            } else {
                mainScanContainer.innerHTML = '<div class="no-scans">No scans available</div>';
                otherScansContainer.innerHTML = '';
            }

        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    }

    function displayPatientInfo(patient) {
        if (!basicInfoElement) return;

        const age = patient.date_of_birth ? calculateAge(patient.date_of_birth) : 'N/A';

        basicInfoElement.innerHTML = `
            <p><strong>${patient.first_name} ${patient.last_name}</strong></p>
            <p>${patient.gender === 'F' ? 'Female' : 'Male'}, ${age} years old</p>
            <p>🔑 ${patient.code || 'N/A'}</p>
            <p>✉️ ${patient.email || 'N/A'}</p>
        `;
    }

    function displayScans(scans) {
        scans.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        scanState.currentMainScan = scans[0];
        scanState.currentOtherScans = scans.slice(1);
        updateScanDisplay();
    }

    function updateScanDisplay() {
        displayMainScan(scanState.currentMainScan);
        displayOtherScans(scanState.currentOtherScans);
    }

    function buildDiagnosisList(predictions) {
        console.log('Raw predictions data:', predictions); // Debug log
        
        if (!predictions) return '<strong>No prediction data available</strong>';
        if (!Array.isArray(predictions)) return '<strong>Invalid prediction format</strong>';
        
        // Debug: Check what fields actually exist in the predictions
        if (predictions.length > 0) {
            console.log('First prediction fields:', Object.keys(predictions[0]));
        }
    
        const filtered = predictions.filter(p => p.confidence > 0.5);
        if (filtered.length === 0) {
            if (predictions.length > 0) {
                return '<strong>Healthy</strong>';
            }
            return '<strong>No predictions available</strong>';
        }
        
        return filtered.map(p => {
            // Try multiple possible field names for disease name
            const diseaseName = p.disease_name || 
                              p.disease || 
                              p.name ||
                              p.label || 
                              'Unknown Disease (check data structure)';
            const confidenceBadge = `<span class="confidence-badge-small" 
                style="background-color: ${getConfidenceColor(p.confidence)}">
                ${Math.round(p.confidence * 100)}%
                </span>`;
            return `<strong>${diseaseName}</strong>: ${confidenceBadge}`;
        }).join('<br>');
    }

    function displayMainScan(scan) {
        if (!mainScanContainer || !scan) {
            mainScanContainer.innerHTML = '<div class="no-scans">No scan selected</div>';
            return;
        }


        const diagnosisText = buildDiagnosisList(scan.predictions);

        mainScanContainer.innerHTML = `
            <div class="main-scan-image-container">
                ${scan.image_scan_url ? `
                    <img src="${scan.image_scan_url}" alt="Main Scan" class="main-scan-image">
                ` : '<div class="no-image">No image available</div>'}
            </div>
            <div class="scan-details-container">
                <h3>Scan Details</h3>
                <div class="detail-row">
                    <span class="detail-label">Organ:</span>
                    <span class="detail-value">${getOrganName(scan.organ)}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Date:</span>
                    <span class="detail-value">${new Date(scan.created_at).toLocaleDateString()}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Diagnosis:</span>
                    <div class="detail-value">${diagnosisText}</div>
                </div>
                ${scan.additional_info ? `
                    <div class="detail-row">
                        <span class="detail-label">Notes:</span>
                        <span class="detail-value">${scan.additional_info}</span>
                    </div>
                ` : ''}
            </div>
        `;
    }

    function displayOtherScans(otherScans) {
        if (!otherScansContainer) return;
        otherScansContainer.innerHTML = '';

        if (!otherScans || otherScans.length === 0) {
            otherScansContainer.innerHTML = '<p>No other scans available</p>';
            return;
        }

        otherScans.forEach(scan => {

            const diagnosisText = buildDiagnosisList(scan.predictions);

            const scanItem = document.createElement('div');
            scanItem.className = 'other-scan-item';
            scanItem.innerHTML = `
                <div class="other-scan-image">
                    ${scan.image_scan_url ? `
                        <img src="${scan.image_scan_url}" alt="Scan">
                    ` : '<div class="no-image-small">No image</div>'}
                </div>
                <div class="other-scan-details">
                    <p><strong>${getOrganName(scan.organ)}</strong></p>
                    <p>${new Date(scan.created_at).toLocaleDateString()}</p>
                    <div class="other-diagnosis">${diagnosisText}</div>
                </div>
            `;

            scanItem.addEventListener('click', () => {
                const previousMain = scanState.currentMainScan;
                scanState.currentMainScan = scan;
                scanState.currentOtherScans = [
                    previousMain,
                    ...scanState.currentOtherScans.filter(s => s.id !== scan.id)
                ];
                updateScanDisplay();
            });

            otherScansContainer.appendChild(scanItem);
        });
    }

    if (submitScanBtn) {
        submitScanBtn.addEventListener('click', async function () {
            if (!selectedFile) {
                alert('Please select a scan file first');
                return;
            }

            try {
                const formData = new FormData();
                formData.append('image_scan_url', selectedFile);
                formData.append('patient', patientId);
                formData.append('organ', organSelect.value);
                formData.append('additional_info', additionalInfo.value);

                const response = await fetch('http://localhost:8000/scans/', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + accessToken,
                    },
                    body: formData
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Upload error details:', errorData);
                    throw new Error(errorData.message || 'Failed to upload scan');
                }

                alert('Scan uploaded successfully!');
                fileInput.value = '';
                previewContainer.style.display = 'none';
                uploadBtn.textContent = 'Upload Scan';
                selectedFile = null;
                additionalInfo.value = '';
                fetchPatientData();

            } catch (error) {
                console.error('Error:', error);
                alert(`Error: ${error.message}`);
            }
        });
    }

    function calculateAge(birthDate) {
        const today = new Date();
        const birthDateObj = new Date(birthDate);
        let age = today.getFullYear() - birthDateObj.getFullYear();
        const monthDiff = today.getMonth() - birthDateObj.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDateObj.getDate())) {
            age--;
        }
        return age;
    }

    function getOrganName(organCode) {
        const organs = { 'H': 'Heart', 'B': 'Brain', 'C': 'Chest' };
        return organs[organCode] || organCode;
    }

    function getConfidenceColor(confidence) {
        if (!confidence) return '#718096';
        if (confidence > 0.7) return '#48bb78';
        if (confidence > 0.4) return '#ed8936';
        return '#e53e3e';
    }

    fetchPatientData();
});