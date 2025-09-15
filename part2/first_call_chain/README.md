# The Developer's Guide to AI - From Prompts to Agents

## Introduction

Converting the Getting Started example to a Langchain call chain.

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

2. Install Python (if necessary)

It's recommended that you setup a virtual environment before installing Python or Python modules.  You can see how to do that here:

[Python Virtual Environment](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#virtual-environment-setup)

If you would rather install Python globally, follow the instructions here:

- Download and install: https://www.python.org/downloads/
- Verify the install in your terminal:

```
~ % python -V
```

- If the installation succeeded, the version will print

3. Install Python modules

- Navigate to the project `part2/first_call_chain` directory in your terminal and run:

```
~/developers-guide-to-ai/part2/first_call_chain % pip install -r requirements.txt
```

- Navigate to the project `part1/client` directory in your terminal and run:

```
~/developers-guide-to-ai/part1/client % npm install
```

4.  Launch the server

- In a terminal, navigate to the `part2/first_call_chain` directory and run the following command:

```
~/developers-guide-to-ai/part2/first_call_chain % fastapi dev main.py
```

5.  Launch the client

- In a separate terminal, navigate to the `part1/client` directory and run the following commands:

```
~/developers-guide-to-ai/part1/client % npm run dev
```

6. Open your web browser and visit: http://localhost:5173

7. Input a question and click `Call your API` to see the response streamed from Llama 3.2 3B