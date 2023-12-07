// main.js
document.addEventListener("DOMContentLoaded", function() {
    var inputField = document.getElementById("feedback-input");
    var sendAction = document.getElementById("send-action");

    inputField.addEventListener("input", function() {
        toggleSendButton();
    });

    sendAction.addEventListener("click", function() {
        if(sendAction.classList.contains("send-enabled")) {
            console.log("Sending:", inputField.value);
            // Add your send logic here
        }
    });

    function toggleSendButton() {
        if(inputField.value.trim() !== "") {
            sendAction.classList.remove("send-disabled");
            sendAction.classList.add("send-enabled");
        } else {
            sendAction.classList.remove("send-enabled");
            sendAction.classList.add("send-disabled");
        }
    }
});

