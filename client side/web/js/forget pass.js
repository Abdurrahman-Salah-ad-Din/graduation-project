function clear_user(){
    document.getElementById("user").value="";
    document.getElementById("user").focus()
}

function check_mail(event){
    let mail = document.getElementById("user").value
    if (mail.slice(-10) != "@email.com"){
        alert("Invalid mail")
    }
    else{
    event.preventDefault(); // Prevent form submission

    let email = document.getElementById("user").value;
    if (email.trim() !== "") {
        localStorage.setItem("userEmail", email); // Store email in localStorage
        window.location.href = "password reset.html"; // Redirect to the next page
    } else {
        alert("Please enter a valid email.");
    }
}
}