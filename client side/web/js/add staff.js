function show_pass(n){
    let eye = document.getElementById(`password_eye${n}`);
    let password = document.querySelector(`.pass${n}`);
    if(password.type == "password"){
        password.type = "text";
        eye.className = "fa-solid fa-eye"
    }
    else{
        password.type = "password";
        eye.className = "fa-solid fa-eye-slash"
    }
    password.focus();

}
    function validatePasswords() {
        const pass1 = document.querySelector('.pass1').value;
        const pass2 = document.querySelector('.pass2').value;
        
        if (pass1 !== pass2) {
            alert("Passwords don't match!");
            return false;
        }
        return `${pass1}`;
    }


// Form submission - wrapped in DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.clear();
            window.location.href = 'login.html';
        });
    }




    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    const userData = JSON.parse(localStorage.getItem('user'));
    const form = document.querySelector('.main-content');

    // Check if form exists before adding listener
    if (!form) {
        console.error("Form element with class 'form' not found!");
        return;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const inputs = document.querySelectorAll("input");
        const selects = document.querySelectorAll("select");
        

        const payload = {
            first_name: inputs[0].value,
            last_name: inputs[1].value,
            job: selects[1].value,
            gender: selects[0].value,
            phone_number: inputs[3].value,
            date_of_birth: inputs[2].value,
            email: inputs[4].value,
            password: validatePasswords(),
            is_staff: true,
            is_active: true,
            is_superuser: true
        };
    
        console.log(payload);
    
        try {
            let response = await fetch('http://localhost:8000/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': "application/json",
                    'Authorization': `Bearer ${accessToken}`
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
                localStorage.setItem('access_token', accessToken);
                localStorage.setItem('refresh_token', refreshToken);
                localStorage.setItem('user', JSON.stringify(userData));
                window.location.href = "staff.html";
                console.log(data.data);
                
            }
        } catch (error) {
            alert(error.message || 'Login failed. Please try again.'); // Simple error handling
        }

    });
});
    
    
    






        