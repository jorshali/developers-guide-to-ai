# The Developer's Guide to AI - From Prompts to Agents

## Getting Started - Section 1: Calling an LLM using an API

Here's how you can start your AI learning journey.

With 10 minutes and basic JavaScript knowledge, you can build a REST service that calls GPT.

5 quick steps will have you:

- Starting a REST service with Express and Node.js
- Using LangChain to connect to Ollama APIs
- Generating a response from a GPT model
- Rendering that response to your browser

It doesn't get any easier to begin your AI learning journey.

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

- Navigate to the project `part1/getting_started/section1` directory in your terminal and run:

```
~/developers-guide-to-ai/part1/getting_started/section1 % npm install
```

4.  Launch the server

- Back in the terminal, run the following command:

```
~/developers-guide-to-ai/part1/getting_started/section1 % node server.mjs
```

- Open your web browser and visit: http://localhost:3000
- You’ll see the response from the Llama model:  test