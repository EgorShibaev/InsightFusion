function rotateLogo(entry) {
    var logo = entry.target;
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;

    // Calculate the horizontal movement and rotation
    var horizontalMovement = scrollY * 0.4; // Adjust the multiplier for speed of movement
    var rotationDegrees = scrollY * 0.4; // Adjust for speed of rotation

    // Determine direction based on logo ID
    var directionMultiplier = logo.id === 'rotating-logo' ? 1 : -1;

    // Apply the horizontal movement and rotation
    logo.style.transform = `translate(${directionMultiplier * horizontalMovement}%, -50%) rotate(${directionMultiplier * rotationDegrees}deg)`;
}

// Set up Intersection Observer
var observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Start rotating when the logo is visible
            window.addEventListener('scroll', () => rotateLogo(entry));
        } else {
            // Optional: Stop the rotation when the logo is not visible
            window.removeEventListener('scroll', () => rotateLogo(entry));
        }
    });
}, { threshold: 0.2 }); // Adjust the threshold as needed

// Observe both logos
document.querySelectorAll('.logo-animation').forEach(logo => {
    observer.observe(logo);
});
