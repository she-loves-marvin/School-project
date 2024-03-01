document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.querySelector('input[type="button"]');
    submitButton.addEventListener('click', processData);
  
  });
  function processData() {
    const email= document.getElementById("email").value;
    const password=document.getElementById("password").value;
    
    if (validateEmail(email) && validatePassword(password)) {
      alert("Logged in successfully");}
    else{
      showError();
    }
}