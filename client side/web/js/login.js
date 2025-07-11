function show_pass(){
    let eye = document.getElementById("password id")
    let password = document.getElementById("pass")
    if(password.type == "password"){
        password.type = "text";
        eye.className = "fa-solid fa-eye"
        document.getElementById("pass").focus();
    }
    else{
        password.type = "password";
        eye.className = "fa-solid fa-eye-slash"
        document.getElementById("pass").focus();
    }
}

function clear_user(){
    document.getElementById("user").value="";
    document.getElementById("user").focus()
}

function check_mail(){
    let mail = document.getElementById("user").value
    if (mail.slice(-10) != "@email.com"){
        alert("Invalid mail")
    }
}

const form = document.querySelector('.form'); // Fix applied here
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        password: document.getElementById("pass").value,
        email: document.getElementById("user").value
    };

    console.log(payload);

    try {
        let response = await fetch('http://127.0.0.1:8000/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.log("Full error response:", errorData); // Add this line
            throw new Error(JSON.stringify(errorData)); // Convert object to string
        }

        const data = await response.json();

        if (data.is_success) {
            localStorage.setItem('access_token', data.data.access);
            localStorage.setItem('refresh_token', data.data.refresh);
            localStorage.setItem('user', JSON.stringify(data.data.radiologist));
            window.location.href = "dashboard.html";
            console.log(data.data);
            
        }
    } catch (error) {
        alert(error.message || 'Login failed. Please try again.'); // Simple error handling
    }
});


