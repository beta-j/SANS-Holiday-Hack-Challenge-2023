//This Code has been generated by OpenAI ChatGPT
//Prompts used are listed in-line at the end

function simulateFishing(iterations) {
let count = 0;

function fishingLoop() {
castReelBtn.click();

// Wait for 'gotone' class to become true
const checkGotOne = setInterval(function () {
if (reelItInBtn.classList.contains('gotone')) {
clearInterval(checkGotOne);
reelItInBtn.click();
count++;

if (count < iterations) {
// Repeat the process
fishingLoop();
}
}
}, 100); // Adjust the interval as needed
}

// Start the fishing loop
fishingLoop();
}

// Example: simulateFishing(5); // Perform the fishing action 5 times

//ChatGPT Prompts used:

//reelItInBtn.click() castReelBtn.click() reelItInBtn.classList.contains('gotone')
//I'd like to write a short JS script that calls the castReelBtn.click() then waits for reelItInBtn.classList.contains('gotone') to become true before calling reelItInBtn.click(). Then repeat the whole thing a number of times
