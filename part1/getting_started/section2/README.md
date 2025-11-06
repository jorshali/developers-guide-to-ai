# The Developer's Guide to AI - From Prompts to Agents

## Getting Started - Section 2: Stream your LLM Responses

The cool typing effect you see in ChatGPT makes it feel responsive.

Without it, the UI would feel slow and often unusable.

OpenAI took a drawback of an LLM, the speed of text generation, and turned it into a killer UI effect.  You can achieve the same responsiveness by streaming LLM responses.
 
When you prompt an LLM, it generates the response in chunks.  Streaming allows you to send these chunks back to the user when they are ready.  As your prompts and chains grow in size and complexity, streaming becomes crucial to performance.

Similar to an infinite scroll, streaming makes LLMs feel infinitely faster to your end users.

With Express and the Ollama SDK it's extremely simple to stream an LLM response from your own REST API.  This tutorial shows you how.

You can access the entire source along with a working UI in the GitHub repository linked in the comments.

## Quick Start

The following steps will get you up and running on your machine.

0. Install Ollama and run:

- Download and install: https://ollama.com
- Verify the install and start Llama in a terminal window:

```
~ % ollama run llama3.2
```

1. Clone this project into a local directory:

```
~ % git clone <url>
```

2. Install Node

- Download and install: https://nodejs.org
- Verify the install in your terminal:

```
~ % node -v
```

- If the installation succeeded, the version will print

3. Install node modules

- Navigate to the project `part1/getting_started/section2` directory in your terminal and run:

```
~/developers-guide-to-ai/part1/getting_started/section2 % npm install
```

- Navigate to the project `part1/client` directory in your terminal and run:

```
~/developers-guide-to-ai/part1/client % npm install
```

4.  Launch the server

- In a terminal, navigate to the `part1/getting_started/section2` directory and run the following command:

```
~/developers-guide-to-ai/part1/getting_started/section2 % node server.mjs
```

5.  Launch the client

- In a separate terminal, navigate to the `part1/client` directory and run the following commands:

```
~/developers-guide-to-ai/part1/client % npm run dev
```

6. Open your web browser and visit: http://localhost:5173

7. Input a question and click `Call your API` to see the response streamed from Llama 3.2 3b