# The Developer's Guide to AI: From Prompts to Agents

## Getting Started - Part 3: Create a RAG solution

Most LLM-powered applications use RAG in some way.

The key to RAG is getting your data to the LLM.  This tutorial shows you how to use a vector search to do just that.

Remember, we're limited on the amount of data we can send to the LLM:

- prompts have a token limit
- LLM providers often charge by the token
- including irrelevant data may confuse the LLM response

We need an efficient way to find only relevant data.

Vector search is a great choice.  We prompt LLMs with natural language and a vector search allows you to find relevant data based on the meaning of what's being asked.

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

- Navigate to the project `part0/simple_rag` directory in your terminal and run:

```
~/ai-for-developers/part0/simple_rag % npm install
```

4.  Launch the server

- Back in the terminal, run the following commands:

```
~/ai-for-developers/part0/simple_rag % node server.mjs
```

5.  Launch the client

- In a terminal, navigate to the `part0/getting_started/client` directory and run the following commands:

```
~/ai-for-developers/client % npm run dev
```

6. Open your web browser and visit: http://localhost:5173

- Type the question into the input:  Can you tell me how to login to Workday?
- The article will be retrieved and passed to the LLM to generate a response