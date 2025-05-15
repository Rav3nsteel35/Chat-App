$(function() {
    $('#sendBtn').bind('click', function() {
        // Get the value from the input field
        var value = document.getElementById('msg').value;
        console.log(value); // Print the value to the console

        // Send the value to the backend
        $.getJSON('/send_message', { val: value }, function(data) {
            console.log(data); // Log the response from the backend
        });

        return false; // Prevent default form submission
    });
});

// function validate(name) {
//     if (name == "") {
//         alert("Name must be filled out");
//         return false;
//     }
//     return true;
// }

window.addEventListener('load', function() {
    // This will be called when the page is fully loaded
    var update_loop = setInterval(fetchMessages, 1000); // Update every 100ms
    console.log("Page loaded successfully!");
    fetchMessages(); // Fetch messages on load
});


function fetchMessages() {
    fetch('/get_messages')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Messages:', data.messages); // Log the messages to the console
        })
        .catch(error => {
            console.error('Error fetching messages:', error);
        });
}

// Call fetchMessages periodically to update the console
// setInterval(fetchMessages, 1000); // Fetch messages every second