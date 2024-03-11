const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid-feedback");
const emailFeedbackArea = document.querySelector(".email-invalid-feedback");
const emailField = document.querySelector("#emailField");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const showPasswordToggleBtn = document.querySelector(".showPasswordToggleBtn");
const passwordField = document.querySelector("#passwordField");
const submitBtn = document.querySelector(".submit-btn");

const handleToogleInputType = (e) => {

    if (showPasswordToggleBtn.textContent === "SHOW") {
        showPasswordToggleBtn.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggleBtn.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggleBtn.addEventListener("click",handleToogleInputType);

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    emailSuccessOutput.textContent= `Checking ${emailVal}`
    emailField.classList.remove("is-invalid");
    emailFeedbackArea.style.display = "none";
    emailSuccessOutput.style.display = "block";
    
    
    if (emailVal.length > 0) {

        fetch("/authentication/validate-email/", {
            body: JSON.stringify({email: emailVal}),method: "POST",
            }).then((res) => res.json()).then((data) => {
                console.log("data", data);
                emailSuccessOutput.style.display = "none";
                if(data.email_error){
                    submitBtn.disabled = true;
                    emailField.classList.add("is-invalid");
                    emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                    emailFeedbackArea.style.display = "block";
                }
                else{
                    submitBtn.disabled = false;
                }
            });
    }
    else{
        emailSuccessOutput.style.display = "none";
    }
});

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.textContent= `Checking ${usernameVal}`
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";
    usernameSuccessOutput.style.display = "block";
    
    if (usernameVal.length > 0) {

        fetch("/authentication/validate-username/", {
            body: JSON.stringify({username: usernameVal}),method: "POST",
            }).then((res) => res.json()).then((data) => {
                console.log("data", data);
                usernameSuccessOutput.style.display = "none";
                if(data.username_error){
                    submitBtn.disabled = true;
                    usernameField.classList.add("is-invalid");
                    feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                    feedbackArea.style.display = "block";
                }else{
                    submitBtn.disabled = false;
                }
            });
        }      
    else{usernameSuccessOutput.style.display = "none";}
});