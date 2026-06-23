console.log("TravelMate Loaded");
const sessionId = crypto.randomUUID();

console.log(
    "Session ID:",
    sessionId
);
const button = document.getElementById("talkBtn");
const transcriptDiv = document.getElementById("transcript");
const responseDiv = document.getElementById("response");
const statusDiv = document.getElementById("status");

let conversationActive = false;
let isSpeaking = false;

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
    recognition.lang = "en-IN";

    button.addEventListener("click", () => {

        if (!conversationActive) {

            conversationActive = true;

            speechSynthesis.cancel();

            statusDiv.innerHTML = "🎤 Listening...";

            button.innerHTML = "⏹️";

            button.classList.add("listening");

            recognition.start();

        } else {

            conversationActive = false;

            speechSynthesis.cancel();

            recognition.stop();

            statusDiv.innerHTML = "✅ Ready";

            button.innerHTML = "🎤";

            button.classList.remove("listening");

            console.log("Conversation stopped");
        }

    });

    recognition.onstart = () => {

        speechSynthesis.cancel();

        isSpeaking = false;

        statusDiv.innerHTML = "🎤 Listening...";

        console.log("Listening started");

    };

    recognition.onend = () => {

        console.log("Listening ended");

        button.classList.remove("listening");

    };

    recognition.onerror = (event) => {

        console.error(
            "Speech Recognition Error:",
            event.error
        );

        statusDiv.innerHTML =
            "❌ Speech Recognition Error";

        button.classList.remove("listening");

        if (conversationActive) {

            setTimeout(() => {

                try {
                    recognition.start();
                } catch {}

            }, 1000);
        }

    };

    recognition.onresult = async (event) => {

        const text =
            event.results[0][0].transcript;

        console.log("User:", text);

        transcriptDiv.innerHTML = text;

        statusDiv.innerHTML =
            "⏳ Thinking...";

        try {

            const response = await fetch(
                "https://travelmate-voice-agent.onrender.com/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    },
                     body: JSON.stringify({
                     message: text,
                     session_id: sessionId
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
                "Assistant:",
                data.response
            );

            responseDiv.innerHTML =
                data.response;

            const cleanText =
                data.response
                    .replace(/[*#`]/g, "")
                    .replace(
                        /[🎉🔥✨🚀😊😂👍❤️😍🥳]/g,
                        ""
                    )
                    .replace(/\n/g, " ")
                    .replace(/\s+/g, " ")
                    .trim();

            const speech =
                new SpeechSynthesisUtterance(
                    cleanText
                );

            speech.rate = 1;
            speech.pitch = 1;
            speech.volume = 1;

            statusDiv.innerHTML =
                "🔊 Speaking...";

            isSpeaking = true;

            speech.onend = () => {

                isSpeaking = false;

                console.log(
                    "Assistant finished speaking"
                );

                if (conversationActive) {

                    statusDiv.innerHTML =
                        "🎤 Listening...";

                    button.classList.add(
                        "listening"
                    );

                    setTimeout(() => {

                        try {
                            recognition.start();
                        } catch (err) {
                            console.log(err);
                        }

                    }, 300);
                }
            };

            speech.onerror = () => {

                isSpeaking = false;

                if (conversationActive) {

                    setTimeout(() => {

                        try {
                            recognition.start();
                        } catch {}

                    }, 300);
                }
            };

            speechSynthesis.cancel();

            speechSynthesis.speak(
                speech
            );

        } catch (error) {

            console.error(
                "Backend Error:",
                error
            );

            responseDiv.innerHTML =
                "Could not connect to backend.";

            statusDiv.innerHTML =
                "❌ Backend Error";

            if (conversationActive) {

                setTimeout(() => {

                    try {
                        recognition.start();
                    } catch {}

                }, 1000);
            }
        }
    };
}