document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('input[type="button"]');
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
    fetch('utilityData.json', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(utilityData),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      console.log('Utility data successfully saved.');
    })
    .catch(error => {
      console.error('There was a problem saving utility data:', error.message);
    });
  }  