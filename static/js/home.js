document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('submitbutton');
    submitButton.addEventListener('click', processData);
  });
  
  function processData() {
    const phoneNumberInput = document.getElementById('phone').value.trim();
    const phoneNumberPattern = /^(07|01)\d{8}$/;
    if (!phoneNumberPattern.test(phoneNumberInput)) {
      alert('Please enter a valid phone number starting with 07 or 01.');
      return;
    }
  
    const amountInput = document.getElementById('amount').value;
    if (!amountInput) {
      alert('Please enter an amount.');
      return;
    }
    const amount = parseFloat(amountInput);
  
    const utilityRows = document.querySelectorAll('#budgetTable tr');
    const utilityData = {};
    utilityData["phonenumber"]=phoneNumberInput;
    utilityData["amount"]=amountInput
  
    utilityRows.forEach(function (row, index) {
      if (index !== 0) {
        const utilityAmount = parseInt(row.querySelector('.utility-amount').value.trim(), 10);
        const utilityTime = row.querySelector('.utility-time').value.trim();
  
        if (!isNaN(utilityAmount)) {
          utilityData[utilityTime] = utilityAmount;
        }
      }
    });
  
    // JSON file
    fetch('https://rocky-wildwood-58249-5658bfaadb54.herokuapp.com/homepage', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },

      body:JSON.stringify(utilityData),
    })
    .then(response => {
      if (!response.ok) {
        alert("Your request was submitted succesfully")
      }
      console.log('Utility data successfully saved.');
    })
    .catch(error => {
      console.error('There was a problem saving utility data:', error.message);
    });
  } 
