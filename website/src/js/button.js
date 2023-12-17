// main.js
document.addEventListener("DOMContentLoaded", function() {
    var inputField = document.getElementById("link-input");
    var sendAction = document.getElementById("send-action");
    var videoPreview = document.getElementById("video-preview");
    var videoStats = document.getElementById("video-stats");
    var info = document.querySelector(".one-more-container");
    var info2 = document.querySelector(".one-more-container-rev");

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
            displayVideoStats(videoId);
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
    }

    function displayVideoStats(videoId) {
        fetch(`http://127.0.0.1:5000/get_stats/${videoId}`, {
            method: 'POST',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("views").innerHTML = data['views']
            document.getElementById("comments").innerHTML = data['comments']
            document.getElementById("likes").innerHTML = data['likes']
            videoStats.style.display = "flex";
        })
        .catch(error => {
            console.log(`Error: ${error}`)
        });
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
            for (let i = 0; i < data.n_of_samples; i++) {
                document.querySelector(`.item.n${i}`).innerHTML = `<p>${data[`cluster_0`][`comment_${i}`]}</p>`;
            }
            document.getElementById("opinion0").innerHTML = `<p>${data[`description_0`]}</p>`;
            document.getElementById("animated-number").innerHTML = data[`number_of_comments_0`];
            info.style.display = "flex";
            // info2.style.display = "flex";
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


function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// const obj = document.getElementById("animated-number");
// animateValue(obj, 32504, 32544, 1000);

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Start the animation when the element is visible
            animateValue(obj, 32544 - 44, 32544, 2500);
            // Optionally, unobserve after the animation starts
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 }); // Adjust the threshold as needed

// observer.observe(obj);
