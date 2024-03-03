document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('sign in button');
    submitButton.addEventListener('click', processData);
  
  });
  function processData() {
    const email= document.getElementById("email").value.trim();
    const password=document.getElementById("password").value.trim();
    if (email === "" || password === "") {
      alert("Please fill in all fields.");
      return;
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
        alert(data.message);
      }
    })
  .catch(error => {
    console.error('There was a problem saving utility data:', error.message);
  });
 
   }

