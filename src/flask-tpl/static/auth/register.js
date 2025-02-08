function pwd_check() {
    let pwd = document.getElementById("password").value;
    let regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
    const span_selector = "div.password-wrapper > span.msg";
    if (!regex.test(pwd)) {
        document.querySelector(span_selector).innerText = "password must contain at least 8 characters, including at least one uppercase letter, one lowercase letter, and one number";
        document.getElementById("password").value = "";
        return false;
    } else {
        document.querySelector(span_selector).innerText = "";
        return true;
    }
}


function pwd_comfirm() {
    let pwd = document.getElementById("password").value;
    let pwd_confirm = document.getElementById("confirm").value;
    const span_selector = "div.confirm-wrapper > span.msg";
    if (pwd != pwd_confirm) {
        document.querySelector(span_selector).innerText = "passwords do not match";
        document.getElementById("confirm").value = "";
        return false;
    } else {
        document.querySelector(span_selector).innerText = "";
        return true;
    }
}