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
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error('Network response was not ok');
      }
    })
    .then(data=>{
      if (data.status==="success"){
        window.location.href = data.redirect_url;
      }
      else{
        alert(data.Data);
      }
    })
    .catch(error => {
    console.error('There was a problem saving utility data:', error.message);
    });
   }
   }

