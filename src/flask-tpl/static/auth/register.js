function pwd_check() {
    let pwd = document.getElementById("password").value;
    let regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
    if (!regex.test(pwd)) {
        document.getElementById("password-msg").innerText = "password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one number";
        document.getElementById("password").value = "";
        return false;
    } else {
        document.getElementById("password-msg").innerText = "";
        return true;
    }
}


function pwd_comfirm() {
    let pwd = document.getElementById("password").value;
    let pwd_confirm = document.getElementById("confirm").value;
    if (pwd != pwd_confirm) {
        document.getElementById("confirm-msg").innerText = "passwords do not match";
        document.getElementById("confirm").value = "";
        return false;
    } else {
        document.getElementById("confirm-msg").innerText = "";
        return true;
    }
}