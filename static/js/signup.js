document.addEventListener('DOMContentLoaded', function () {
  const submitButton = document.getElementById('submitbutton');
  submitButton.addEventListener('click', processData);

});
function processData() {
  const email= document.getElementById("Email address").value.trim();
  const password=document.getElementById("Password").value.trim();
  const confirmpassword=document.getElementById("confirm password").value.trim();
  if (email === "" || password === "" || confirmpassword === "") {
    alert("Please fill in all fields.");
    return;
  }
  else if(password!==confirmpassword){
      alert("Passwords do not match")
      return;
  }
  else{
    const data= {
      "Email": email,
      "Password": password,
    };
    fetch('https://rocky-wildwood-58249-5658bfaadb54.herokuapp.com/signup',{
      method:'POST',
      headers:{
        'content-Type':'application/json'
      },
      body:JSON.stringify(data)
    })
    .then(response =>response.json() )
    .then(data => {
      const value = data.Data;
      alert(value);
    })
    .catch(error => {
    console.error('There was a problem saving utility data:', error.message);
    });
   }
   }

