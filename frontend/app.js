console.log("TravelMate Loaded");

const button = document.getElementById("talkBtn");
const transcriptDiv = document.getElementById("transcript");
const responseDiv = document.getElementById("response");
const statusDiv = document.getElementById("status");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (!SpeechRecognition) {

    alert(
        "Speech Recognition is not supported in this browser.\nUse Google Chrome."
    );

} else {

    const recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    button.addEventListener("click", () => {

        responseDiv.innerHTML = "";
        statusDiv.innerHTML = "🎤 Listening...";

        button.classList.add("listening");

        recognition.start();

    });

    recognition.onstart = () => {

        console.log("Listening started");

    };

    recognition.onend = () => {

        button.classList.remove("listening");

        console.log("Listening ended");

    };

    recognition.onerror = (event) => {

        console.error("Speech Error:", event.error);

        statusDiv.innerHTML =
            "❌ Speech recognition error";

        button.classList.remove("listening");

    };

    recognition.onresult = async (event) => {

        const text =
            event.results[0][0].transcript;

        console.log("User said:", text);

        transcriptDiv.innerHTML = text;

        statusDiv.innerHTML =
            "⏳ Processing...";

        try {

            const response = await fetch(
                "http://127.0.0.1:8000/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        message: text
                    })
                }
            );

            if (!response.ok) {

                throw new Error(
                    `HTTP Error ${response.status}`
                );

            }

            const data =
                await response.json();

            console.log(
                "Backend Response:",
                data
            );

            responseDiv.innerHTML =
                data.response;

            statusDiv.innerHTML =
                "✅ Ready";

            const speech =
                new SpeechSynthesisUtterance(
                    data.response
                );

            speech.rate = 1;
            speech.pitch = 1;
            speech.volume = 1;

            speechSynthesis.speak(
                speech
            );

        } catch (error) {

            console.error(
                "Fetch Error:",
                error
            );

            responseDiv.innerHTML =
                "Could not connect to backend.";

            statusDiv.innerHTML =
                "❌ Backend Error";
        }
    };
}