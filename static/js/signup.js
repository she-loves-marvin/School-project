let FormData =[];
const Addformdata = (ev)=>{
  ev.preventDefault();
  let FormData= {
     PhoneNumber:document.getElementById("PhoneNumber").Value,
     email:document.getElementById("email").value,
     Password:document.getElementById("Password").value,
     ConfirmPassword :document.getElementById("ConfirmPassword").value
}
FormData.push(FormData);
console.log(FormData);
document.querySelector('form').reset()
}