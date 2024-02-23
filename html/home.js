// Function to update balance dynamically
function updateBalance(newBalance) {
    document.getElementById('balance').innerText = 'Balance Left: ' + newBalance + ' ksh';
  }
  
  // Function to update table contents based on user input
  function updateTable() {
    // Retrieve user input
    var phoneNumber = document.getElementById('phone').value;
  
    // Check if phone number starts with 07 or 01
    if (!(phoneNumber.startsWith('07') || phoneNumber.startsWith('01'))) {
      alert('Phone number must start with 07 or 01');
      return;
    }
  
    // Example: Update time for each utility
    var utilities = ['electricity', 'internet', 'water', 'gas', 'rent'];
    for (var i = 0; i < utilities.length; i++) {
      var utility = utilities[i];
      var utilityTime = Math.floor(Math.random() * 24) + ' hours'; // Example: Generate random time
      document.getElementById(utility + 'Time').innerText = utilityTime;
    }
  
    // Example: Update balance (randomly generated)
    var newBalance = Math.floor(Math.random() * 1000) + 500; // Example: Generate random balance
    updateBalance(newBalance);
  }
  
  // Attach event listener to input field for dynamic updates
  document.getElementById('phone').addEventListener('input', updateTable);
  