# The Developer's Guide to AI - From Prompts to Agents

## Introduction

A set of Python scripts that demonstrate RAG concepts by experimenting with chunking strategies and building various versions of a chatbot grounded on the example documentation.  Also includes a FastAPI server for the chatbot that implements a conversational RAG (Retrieval-Augmented Generation) system. The examples combine the Ollama SDK with a vector store to retrieve relevant documents to provide context-aware responses.

## Prerequisites

The following steps will get you up and running on your machine.

Install Ollama (if necessary):

- Follow the instructions in: [Install Ollama](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-ollama)

Install Python (if necessary):

- Follow the instructions in: [Install Python](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-python-if-necessary)

Navigate to the project (e.g. `part3/rag_examples`) directory in your terminal and run:

```
~/ai-for-devs/part3/rag_examples % python -m pip install -r requirements.txt
```

## Run a Python Script

In a terminal, navigate to the project directory (e.g. `part3/rag_examples`) and run the following command:

```
~/ai-for-devs/part3/rag_examples % python create_chat_request.py
```

## Start the Chatbot

Start the book example documentation chatbot to interact with your local Ollama server.

### Start the Server

In a terminal, navigate to the project directory (e.g. `part3/rag_examples`) and run the following command:

```
~/ai-for-devs/part3/rag_examples % fastapi dev main.py
```

### Start the Client

In a separate terminal, navigate to the `part3/client` directory and run the following commands:

```
~/ai-for-devs/part1/client % npm install
~/ai-for-devs/part1/client % npm run dev
```

Open your web browser and visit: http://localhost:5173

Input a question about the book examples documentation and press `Enter` to see the response streamed from Llama 3.2 3B.

Ask a follow up question and notice how the example support chatbot remembers the conversation.