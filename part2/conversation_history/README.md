# The Developer's Guide to AI - From Prompts to Agents

## Introduction

A set of Python scripts that demonstrate conversation history concepts.  Includes a simple FastAPI server implementation for a simple conversational chatbot using the Ollama SDK.

## Prerequisites

The following steps will get you up and running on your machine.

Install Ollama (if necessary):

- Follow the instructions in: [Install Ollama](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-ollama)

Install Python (if necessary):

- Follow the instructions in: [Install Python](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-python-if-necessary)

Navigate to the project (e.g. `part2/conversation_history`) directory in your terminal and run:

```
~/ai-for-devs/part2/conversation_history % python -m pip install -r requirements.txt
```

## Run a Python Script

In a terminal, navigate to the project directory (e.g. `part2/conversation_history`) and run the following command:

```
~/ai-for-devs/part2/conversation_history % python create_chat_request.py
```

## Start the Chatbot

Start a simple conversational chatbot to interact with your local Ollama server.

### Start the Server

In a terminal, navigate to the project directory (e.g. `part2/conversation_history`) and run the following command:

```
~/ai-for-devs/part2/conversation_history % fastapi dev main.py
```

### Start the Client

In a separate terminal, navigate to the `part2/client` directory and run the following commands:

```
~/ai-for-devs/part1/client % npm install
~/ai-for-devs/part1/client % npm run dev
```

Open your web browser and visit: http://localhost:5173

Input a question and press `Enter` to see the response streamed from Llama 3.2 3B.

Ask a follow up question and notice how the chatbot remembers the conversation.