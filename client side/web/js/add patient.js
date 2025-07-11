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
    let patientData;

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

    if (!accessToken) {
        alert("No access token found. Please login.");
        window.location.href = 'login.html';
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        try {
            const inputs = form.querySelectorAll("input, select, textarea");
            const patientPayload = {
                email: inputs[5].value.trim(),
                first_name: inputs[0].value.trim(),
                last_name: inputs[1].value.trim(),
                date_of_birth: inputs[2].value,
                gender: inputs[3].value === "male" ? "M" : "F",
                phone_number: inputs[4].value
            };

            if (!patientPayload.email || !patientPayload.phone_number) {
                throw new Error('Email and phone number are required');
            }

            const patientResponse = await fetch('http://localhost:8000/patients/', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer ' + accessToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(patientPayload)
            });

            if (!patientResponse.ok) {
                const errorData = await patientResponse.json();
                throw new Error(errorData.message || 'Failed to create patient');
            }

            patientData = await patientResponse.json();
            console.log("Patient created:", patientData);

            // ✅ Encode image and send as base64 if selected
            if (selectedFile) {
                const formData = new FormData();
    
                // Append the file directly
                formData.append('image_scan_url', selectedFile);
                
                const organ = document.getElementById('organSelect').value;
                let add_info = document.querySelector('.additional-info').value;
            
                // Append other fields
                formData.append('patient', patientData.data.id);
                formData.append('organ', `${organ}`);
                formData.append('additional_info', `${add_info}`);


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
            }

            alert('Patient and scan saved successfully!');
            form.reset();
            previewContainer.style.display = 'none';
            uploadButton.textContent = 'Upload Scan';
            selectedFile = null;

        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        }
    });
});
