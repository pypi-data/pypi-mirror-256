// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  if (!window.rendered) {
    // Grab the label and default value that the user specified
    const {label, value} = event.detail.args;

    // Set the label text to be what the user specified
    const label_el = document.getElementById("label")
    label_el.innerText = label

    // Set the default value to be what the user specified
    const input = document.getElementById("input_box");
    if (value) {
      input.value = value
    }

    // On the keyup event, send the new value to Python
    input.onkeyup = event => sendValue(event.target.value)


    const startButton = document.getElementById('startButton');
    const playButton = document.getElementById('playButton');
    const messageContainer = document.getElementById('messageContainer');
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    let isRecording = false;
    let recordedSpeech = '';

    recognition.interimResults = true;
    recognition.continuous = true;

    startButton.addEventListener('click', () => {
        toggleRecording();
    });

    playButton.addEventListener('click', () => {
        if (recordedSpeech) {
            textToSpeech(recordedSpeech);
        } else {
            console.log('No recording available.');
        }
    });

    function toggleRecording() {
        if (isRecording) {
            stopRecognition();
        } else {
            startRecognition();
        }
    }

    function startRecognition() {
        recognition.start();
        isRecording = true;
        startButton.textContent = 'Stop Recording';
    }

    function stopRecognition() {
        recognition.stop();
        isRecording = false;
        startButton.textContent = 'Start Recording';
    }

    function textToSpeech(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        const voices = speechSynthesis.getVoices();
        utterance.voice = voices[0];
        speechSynthesis.speak(utterance);
    }

    recognition.onresult = event => {
        const result = event.results[event.results.length - 1][0].transcript;
        messageContainer.textContent = result;
        recordedSpeech = result;
        if (result.trim().length > 0) {
            playButton.style.display = 'inline-block'; // Display play button if recognized text is available
        }
    };

    recognition.onend = () => {
        if (isRecording) {
            startRecognition(); // Restart recognition if it was not manually stopped
        }
    };

    recognition.onerror = event => {
        console.error('Speech recognition error:', event.error);
    };

    recognition.onnomatch = () => {
        console.log('No speech was recognized.');
    };

    
    window.rendered = true
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(100)

Streamlit.setFrameHeight(85)


