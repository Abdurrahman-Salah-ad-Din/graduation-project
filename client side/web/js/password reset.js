function show_pass(){
    let eye = document.getElementById("password id")
    let password = document.getElementById("password")
    if(password.type == "password"){
        password.type = "text";
        eye.className = "fa-solid fa-eye"
        document.getElementById("user").focus();
    }
    else{
        password.type = "password";
        eye.className = "fa-solid fa-eye-slash"
        document.getElementById("user").focus();
    }
}


function check_mail(){
    let mail = document.getElementById("user").value
    if (mail.slice(-10) != "@email.com"){
        alert("Invalid mail")
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let email = localStorage.getItem("userEmail");
    if (email) {
        document.getElementById("email-display").innerText = `We have sent a code to ${email}.`;
    }
});
