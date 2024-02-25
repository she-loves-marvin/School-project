document.addEventListener('DOMContentLoaded', function () {
  const submitButton = document.querySelector('input[type="button"]');
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
  const utilityData = [];

  utilityRows.forEach(function (row, index) {
      if (index !== 0) {
          const utilityName = row.querySelector('.utility-name').value.trim();
          const utilityAmount = row.querySelector('.utility-amount').value.trim();
          const utilityTime = row.querySelector('.utility-time').value.trim();

          utilityData.push({
              name: utilityName,
              amount: utilityAmount,
              time: utilityTime
          });
      }
  });

  console.log('Phone Number:', phoneNumberInput);
  console.log('Amount:', amount);
  console.log('Utility Data:', utilityData);
}

