from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"hi|hello|hey",
        ["Hello!", "Hey there!", "Hi! How can I help you today?"]
    ],
    [
        r"how are you ?",
        ["I'm doing well, thank you!", "I'm great, thanks for asking!"]
    ],
    [
        r"(.*) your name ?",
        ["You can call me Chatbot.", "I go by the name Chatbot."]
    ],
    [
        r"quit",
        ["Bye, take care!", "Goodbye!", "See you later!"]
    ],
    [
        r'maha',
        ["Maha is a great person!"]
    ],
    [
        r'How are you',
        ["Im great,what about you..!"]
    ]
]

def create_chatbot():
    return Chat(pairs, reflections)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Chatbot</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Chatbot</h1>
                </header>
                <div id="chat-container">
                    <div id="chat-box"></div>
                    <input type="text" id="user-input" placeholder="Type your message...">
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
            <script>
                const chatBox = document.getElementById('chat-box');

                function appendMessage(message, sender) {
                    const messageElement = document.createElement('div');
                    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                    messageElement.innerText = message;
                    chatBox.appendChild(messageElement);
                    chatBox.scrollTop = chatBox.scrollHeight;
                }

                async function sendMessage() {
                    const userInput = document.getElementById('user-input');
                    const message = userInput.value.trim();
                    if (message !== '') {
                        appendMessage('You: ' + message, 'user');
                        userInput.value = '';

                        const response = await fetch('/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            body: 'message=' + encodeURIComponent(message)
                        });
                        const data = await response.text();
                        appendMessage('Chatbot: ' + data, 'bot');
                    }
                }

                // Initial message
                appendMessage('Chatbot: Hello! I am a chatbot. You can ask me anything.', 'bot');
            </script>
        </body>
        </html>
    """

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    chatbot = create_chatbot()
    response = chatbot.respond(message.lower())
    return response if response else "Sorry, I didn't understand that."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
