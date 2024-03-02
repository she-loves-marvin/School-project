document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('sign in button');
    submitButton.addEventListener('click', processData);
  
  });
  function processData() {
    const email= document.getElementById("email").value.trim();
    const password=document.getElementById("password").value.trim();
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
    .then(response =>response.json() )
  .then(data => {
    const value = data.value;
    alert(value);
  })
  .catch(error => {
    console.error('There was a problem saving utility data:', error.message);
  });
 
   }

