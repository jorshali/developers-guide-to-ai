# The Developer's Guide to AI - From Prompts to Agents

## Introduction

The cool typing effect you see in ChatGPT makes it feel responsive.

Without it, the UI would feel slow and often unusable.

OpenAI took a drawback of an LLM, the speed of text generation, and turned it into a killer UI effect.  You can achieve the same responsiveness by streaming LLM responses.
 
When you prompt an LLM, it generates the response in chunks.  Streaming allows you to send these chunks back to the user when they are ready.  As your prompts and chains grow in size and complexity, streaming becomes crucial to performance.

Similar to an infinite scroll, streaming makes LLMs feel infinitely faster to your end users.

With Express and the Ollama SDK it's extremely simple to stream an LLM response from your own REST API.  This tutorial shows you how.

You can access the entire source along with a working UI in the GitHub repository linked in the comments.

## Prerequisites

The following steps will get you up and running on your machine.

Install Ollama (if necessary):

- Follow the instructions in: [Install Ollama](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-ollama)

Install Node (if necessary):

- Download and install: https://nodejs.org

## Start the Server

In a terminal, navigate to the `part1/getting_started/section2` directory and run the following commands:

```
~/ai-for-devs/part1/getting_started/section2 % npm install
~/ai-for-devs/part1/getting_started/section2 % node server.mjs
```

## Start the Client

In a separate terminal, navigate to the `part1/client` directory and run the following commands:

```
~/ai-for-devs/part1/client % npm install
~/ai-for-devs/part1/client % npm run dev
```

Open your web browser and visit: http://localhost:5173

Input a question and click `Call your API` to see the response streamed from Llama 3.2.