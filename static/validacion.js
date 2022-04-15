function validation() {
    var form = document.getElementById("login-form")
    var password = document.getElementById("password").value
    var text = document.getElementById("text")
    var pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (password.match(pattern)) 
    {
        form.classList.add("valid");
        form.classList.remove("invalid");
    }
    else 
    {
        form.classList.remove("valid");
        form.classList.add("invalid");
    }
}