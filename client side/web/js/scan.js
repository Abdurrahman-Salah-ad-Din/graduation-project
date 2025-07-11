document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.clear();
            window.location.href = 'login.html';
        });
    }

    const form = document.querySelector(".patient-form");
    const accessToken = localStorage.getItem("access_token");
    let selectedFile = null;

    // Get patient ID from URL first
    const urlParams = new URLSearchParams(window.location.search);
    const patientId = urlParams.get('patient_id');
    
    if (!patientId) {
        console.error('No patient ID found in URL');
        alert('No patient specified. Redirecting back to patient list.');
        window.location.href = 'patients.html';
        return;
    }

    if (!accessToken) {
        alert("No access token found. Please login.");
        window.location.href = 'login.html';
        return;
    }

    // File upload setup
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);

    const uploadButton = document.querySelector('.upload-btn');
    const previewContainer = document.createElement('div');
    previewContainer.className = 'preview-container';
    previewContainer.style.display = 'none';

    const previewImage = document.createElement('img');
    previewImage.className = 'preview-image';
    previewImage.alt = 'Preview';

    const fileInfo = document.createElement('div');
    fileInfo.className = 'file-info';

    previewContainer.appendChild(previewImage);
    previewContainer.appendChild(fileInfo);
    uploadButton.parentNode.appendChild(previewContainer);

    fileInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
            selectedFile = this.files[0];
            uploadButton.textContent = 'Change Scan';

            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewContainer.style.display = 'block';
                fileInfo.textContent = `File: ${selectedFile.name} (${(selectedFile.size / 1024).toFixed(1)} KB)`;
            };
            reader.readAsDataURL(selectedFile);
        } else {
            selectedFile = null;
            previewContainer.style.display = 'none';
            uploadButton.textContent = 'Upload Scan';
        }
    });

    uploadButton.addEventListener('click', () => fileInput.click());

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        try {
            // Check if a file was selected
            if (!selectedFile) {
                throw new Error('Please select a scan file to upload');
            }

            // Get form values
            const organSelect = document.getElementById('organSelect');
            const additionalInfo = document.querySelector('.additional-info');
            
            if (!organSelect || !additionalInfo) {
                throw new Error('Required form elements not found');
            }

            const organ = organSelect.value;
            const add_info = additionalInfo.value;

            // Create FormData
            const formData = new FormData();
            formData.append('image_scan_url', selectedFile);
            formData.append('patient', patientId); // Use the patientId from URL
            formData.append('organ', organ);
            formData.append('additional_info', add_info);

            const scanResponse = await fetch('http://localhost:8000/scans/', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + accessToken,
                },
                body: formData
            });

            if (!scanResponse.ok) {
                const errorData = await scanResponse.json();
                throw new Error(errorData.message || 'Failed to upload scan');
            }

            const scanData = await scanResponse.json();
            console.log("Scan uploaded:", scanData);

            alert('Scan saved successfully! Redirecting to patient page...');
            
            // Redirect to view patient.html with the patient ID
            window.location.href = `view patient.html?id=${patientId}`;

        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    });
});