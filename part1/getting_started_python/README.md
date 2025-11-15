# The Developer's Guide to AI - From Prompts to Agents

## Introduction

Porting the Getting Started example to Python.

## Prerequisites

The following steps will get you up and running on your machine.

Install Ollama (if necessary):

- Follow the instructions in: [Install Ollama](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-ollama)

Install Python (if necessary):

- Follow the instructions in: [Install Python](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#install-python-if-necessary)

Navigate to the project (e.g. `part1/getting_started_python`) directory in your terminal and run:

```
~/ai-for-devs/part1/getting_started_python % python -m pip install -r requirements.txt
```

### Start the Server

In a terminal, navigate to the project directory (e.g. `part1/getting_started_python`) and run the following command:

```
~/ai-for-devs/part1/getting_started_python % fastapi dev main.py
```

### Start the Client

In a separate terminal, navigate to the `part1/client` directory and run the following commands:

```
~/ai-for-devs/part1/client % npm install
~/ai-for-devs/part1/client % npm run dev
```

Open your web browser and visit: http://localhost:5173

Input a question and click `Call your API` to see the response streamed from Llama 3.2.