// Sound mapping object
const sound = {
    65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
    87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
    83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
    69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
    68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
    70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
    84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
    71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
    89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
    72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
    85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
    74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
    75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
    79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
    76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
    80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
    186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

// Track the sequence of keys pressed
let keySequence = "";
let isAwakened = false;

// Play sound function
const playSound = (keyCode) => {
    if (sound[keyCode] && !isAwakened) {
        const audio = new Audio(sound[keyCode]);
        audio.play();
    }
};

// Visual feedback for key press
const pressKey = (keyElement) => {
    if (keyElement && !isAwakened) {
        keyElement.classList.add('active');
        setTimeout(() => {
            keyElement.classList.remove('active');
        }, 200);
    }
};

// Awaken the Great Old One
const awakenGreatOldOne = () => {
    if (isAwakened) return;
    
    isAwakened = true;
    
    console.log("The Great Old One awakens!");
    
    // Fade out the piano
    const pianoWrapper = document.getElementById('piano-wrapper');
    pianoWrapper.classList.add('fade-out');
    
    // Show the Great Old One image after delay
    setTimeout(() => {
        const greatOldOne = document.getElementById('great-old-one');
        greatOldOne.classList.remove('hidden');
        
        setTimeout(() => {
            greatOldOne.classList.add('show');
        }, 100);
        
        // Play creepy audio - using the correct URL you provided
        const creepyAudio = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3');
        creepyAudio.volume = 0.7;
        creepyAudio.play().catch(err => {
            console.log("Audio playback failed:", err);
        });
    }, 1000);
};

// Check if "weseeyou" sequence was typed
const checkSequence = (key) => {
    // Only add alphabetic keys to sequence
    if (/^[a-zA-Z]$/.test(key)) {
        keySequence += key.toLowerCase();
        
        // Keep only last 8 characters
        if (keySequence.length > 8) {
            keySequence = keySequence.slice(-8);
        }
        
        console.log("Current sequence:", keySequence);
        
        // Check if sequence matches "weseeyou"
        if (keySequence === "weseeyou") {
            awakenGreatOldOne();
        }
    }
};

// Keyboard event listener
document.addEventListener('keydown', (e) => {
    const keyCode = e.keyCode;
    const key = e.key;
    
    // Find the corresponding piano key element
    const keyElement = document.querySelector(`.key[data-key="${keyCode}"]`);
    
    if (keyElement && !isAwakened) {
        // Prevent default to avoid page scrolling
        e.preventDefault();
        
        // Play sound
        playSound(keyCode);
        
        // Visual feedback
        pressKey(keyElement);
    }
    
    // Always check sequence for awakening
    checkSequence(key);
});

// Mouse hover events for key labels
const piano = document.getElementById('piano');
const keys = document.querySelectorAll('.key');

// Additional mouse click support
keys.forEach(key => {
    key.addEventListener('click', () => {
        if (!isAwakened) {
            const keyCode = parseInt(key.getAttribute('data-key'));
            playSound(keyCode);
            pressKey(key);
        }
    });
});