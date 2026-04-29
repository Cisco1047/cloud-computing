const cookieContainer = document.getElementById('cookie');
const paperContainer = document.getElementById('paper');
const fortuneText = document.getElementById('fortuneMessage');
const resetButton = document.getElementById('resetBtn');

const API_ENDPOINT = 'https://ytiioq3g99.execute-api.us-east-1.amazonaws.com/api/fortune';

async function crackCookie() {
    // Prevent double clicking while open
    if (cookieContainer.classList.contains('open')) return;

    // 1. Trigger the CSS 'crack' animation (cookie halves fly apart)
    cookieContainer.classList.add('open');

    // 2. Fetch the fortune immediately (happens while animation runs)
    try {
        const response = await fetch(API_ENDPOINT);
        const data = await response.json();

        // Populate the paper with the DynamoDB fortune
        fortuneText.innerText = data.fortune || "Your future holds unexpected joy.";

    } catch (error) {
        console.error("The fates are silent:", error);
        fortuneText.innerText = "The cloud is hazy. A try again is wise.";
    }

    // 3. Reveal the paper after a slight delay for the 'crack' moment
    setTimeout(() => {
        paperContainer.classList.add('reveal');
        resetButton.classList.remove('hidden');
    }, 450); // Matches the satisfying impact of the CSS easing
}

function resetFate() {
    // 1. Hide the paper and reset button
    paperContainer.classList.remove('reveal');
    resetButton.classList.add('hidden');

    // 2. Clear the old fortune text (so it doesn't blink next time)
    fortuneText.innerText = "Reading the stars...";

    // 3. Close the cookie halves after the paper is hidden
    setTimeout(() => {
        cookieContainer.classList.remove('open');
    }, 300);
}

// Attach listeners
cookieContainer.addEventListener('click', crackCookie);
resetButton.addEventListener('click', resetFate);