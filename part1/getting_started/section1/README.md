# The Developer's Guide to AI - From Prompts to Agents

## Introduction

Here's how you can start your AI learning journey.

With 10 minutes and basic JavaScript knowledge, you can build a REST service that calls GPT.

5 quick steps will have you:

- Starting a REST service with Express and Node.js
- Using the Ollama SDK to connect to Ollama APIs
- Generating a response from a GPT model
- Rendering that response to your browser

It doesn't get any easier to begin your AI learning journey.

## Prerequisites

The following steps will get you up and running on your machine.

Install Ollama (if necessary):

- Follow the instructions in: [Install Ollama](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-ollama)

Install Node (if necessary):

- Download and install: https://nodejs.org

## Start the Server

In a terminal, navigate to the `part1/getting_started/section1` directory and run the following commands:

```
~/developers-guide-to-ai/part1/getting_started/section1 % npm install
~/developers-guide-to-ai/part1/getting_started/section1 % node server.mjs
```

Open your web browser and visit: http://localhost:8000

You’ll see the response from the Llama 3.2 model:  `test`