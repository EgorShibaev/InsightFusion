// main.js
document.addEventListener("DOMContentLoaded", function() {
    var inputField = document.getElementById("link-input");
    var sendAction = document.getElementById("send-action");
    var videoPreview = document.getElementById("video-preview");
    var videoStats = document.getElementById("video-stats");
    var carousel = document.querySelector(".carousel-container");

    inputField.addEventListener("input", function() {
        toggleSendButton();
    });

    sendAction.addEventListener("click", function() {
        if(sendAction.classList.contains("send-enabled")) {
            var videoUrl = inputField.value;
            var videoId = extractYoutubeVideoId(videoUrl);
            if (!videoId) {
                console.log("Invalid YouTube URL");
                return;
            }
            displayVideoPreview(videoId);
            displayComments(videoId);
        }
    });

    function extractYoutubeVideoId(url) {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        var match = url.match(regExp);

        if (match && match[2].length == 11) {
            return match[2];
        } else {
            return null;
        }
    }

    function toggleSendButton() {
        if(inputField.value.trim() !== "") {
            sendAction.classList.remove("send-disabled");
            sendAction.classList.add("send-enabled");
        } else {
            sendAction.classList.remove("send-enabled");
            sendAction.classList.add("send-disabled");
        }
    }

    function displayVideoPreview(videoId) {
        videoPreview.innerHTML = '<iframe width="720" height="405" src="https://www.youtube.com/embed/' + videoId + '" frameborder="0" allowfullscreen></iframe>';
        videoStats.style.display = "flex";
    }

    function displayComments(videoId) {
        fetch(`http://127.0.0.1:5000/analyze_comments/${videoId}`, {
            method: 'POST',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.querySelector(".item.a").innerHTML = `<p>${data.description_0}</p>`;
            document.querySelector(".item.b").innerHTML = `<p>${data.description_1}</p>`;
            document.querySelector(".item.c").innerHTML = `<p>${data.description_2}</p>`;
            document.querySelector(".item.d").innerHTML = `<p>${data.description_3}</p>`;
            document.querySelector(".item.e").innerHTML = `<p>${data.description_4}</p>`;
            document.querySelector(".item.f").innerHTML = `<p>${data.description_5}</p>`;
            carousel.style.display = "flex";
        })
        .catch(error => {
            console.log(`Error: ${error}`)
        });
    }
});

$(document).ready(function() {
    var carousel = $(".carousel");
    var currdeg = 0;
    var itemWidth = 250; // Width of each item in pixels

    // Attach click event to each carousel item
    $(".item").on("click", function() {
        rotateCarousel();
    });

    function rotateCarousel() {
        currdeg -= 60; // Assuming each item rotates the carousel by 60 degrees
        carousel.css({
            "-webkit-transform": "rotateY(" + currdeg + "deg)",
            "-moz-transform": "rotateY(" + currdeg + "deg)",
            "-o-transform": "rotateY(" + currdeg + "deg)",
            "transform": "rotateY(" + currdeg + "deg)"
        });
    }
});


