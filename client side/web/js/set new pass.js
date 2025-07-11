function show_pass(x){
    let eye = document.getElementById(`password_eye${x}`)
    let password = document.getElementById(`pass${x}`)
    if(password.type == "password"){
        password.type = "text";
        eye.className = "fa-solid fa-eye"
        document.getElementById(`pass${x}`).focus();
    }
    else{
        password.type = "password";
        eye.className = "fa-solid fa-eye-slash"
        document.getElementById(`pass${x}`).focus();
    }
}