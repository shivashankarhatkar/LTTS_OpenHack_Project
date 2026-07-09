/*
==========================================================
Enterprise Knowledge Assistant
app.js
==========================================================
*/

const API_BASE = "http://localhost:8000/api/v1";

const chatForm = document.getElementById("chat-form");
const queryInput = document.getElementById("query");
const sendButton = document.getElementById("send-button");

const chatContainer = document.getElementById("chat-container");

const confidenceElement = document.getElementById("confidence");
const validationElement = document.getElementById("validation");
const citationsElement = document.getElementById("citations");

const connectionStatus = document.getElementById(
    "connection-status",
);

async function checkHealth() {

    try {

        const response = await fetch(
            `${API_BASE}/health`,
        );

        if (!response.ok) {

            throw new Error();

        }

        connectionStatus.textContent = "Connected";

        connectionStatus.classList.remove(
            "disconnected",
        );

        connectionStatus.classList.add(
            "connected",
        );

    }

    catch {

        connectionStatus.textContent =
            "Disconnected";

        connectionStatus.classList.remove(
            "connected",
        );

        connectionStatus.classList.add(
            "disconnected",
        );

    }

}

function addMessage(
    sender,
    text,
) {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        sender === "user"
            ? "user-message"
            : "assistant-message";

    const header =
        document.createElement("div");

    header.className =
        "message-header";

    header.textContent =
        sender === "user"
            ? "You"
            : "Assistant";

    const body =
        document.createElement("div");

    body.className =
        "message-body";

    body.textContent = text;

    wrapper.appendChild(header);

    wrapper.appendChild(body);

    chatContainer.appendChild(wrapper);

    chatContainer.scrollTop =
        chatContainer.scrollHeight;
}

function updateSidebar(
    response,
) {

    confidenceElement.textContent =
        `${Math.round(
            response.confidence * 100,
        )}%`;

    validationElement.textContent =
        response.validation_message;

    citationsElement.innerHTML = "";

    response.citations.forEach(
        citation => {

            const li =
                document.createElement("li");

            li.innerHTML = `
                <strong>${citation.title}</strong><br>
                ${citation.reference}<br>
                <small>
                    ${citation.source_type}
                </small>
            `;

            citationsElement.appendChild(
                li,
            );

        },
    );

}

async function askQuestion(
    question,
) {

    sendButton.disabled = true;

    sendButton.textContent = "Thinking...";

    addMessage(
        "user",
        question,
    );

    try {

        const response =
            await fetch(
                `${API_BASE}/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify(
                        {
                            query: question,

                            top_k: 5,
                        },
                    ),
                },
            );

        if (!response.ok) {

            throw new Error(
                "Server Error",
            );

        }

        const data =
            await response.json();

        addMessage(
            "assistant",
            data.answer,
        );

        updateSidebar(
            data,
        );

    }

    catch (error) {

        addMessage(
            "assistant",
            "Unable to contact the backend.",
        );

        console.error(
            error,
        );

    }

    finally {

        sendButton.disabled = false;

        sendButton.textContent = "Send";

    }

}

chatForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();

        const question =
            queryInput.value.trim();

        if (!question) {

            return;

        }

        queryInput.value = "";

        await askQuestion(
            question,
        );

    },
);

checkHealth();

setInterval(
    checkHealth,
    30000,
);