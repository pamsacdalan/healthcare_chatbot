
    document.addEventListener("DOMContentLoaded", () => {
        const spinner = document.querySelector(".spinner");
        const spinnerContainer = document.getElementById("spinner-container");

        // Show the spinner
        spinnerContainer.style.display = 'block';

        spinner.addEventListener("animationend", () => {
            // Remove the spinner container when the animation ends
            spinnerContainer.remove();
        });
    });

