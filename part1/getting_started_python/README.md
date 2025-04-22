# The Developer's Guide to AI - From Prompts to Agents

## Python Primer

Porting the Getting Started example to Python.

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

- Download and install: https://www.python.org/downloads/
- Verify the install in your terminal:

```
~ % python -V
```

- If the installation succeeded, the version will print

3. Install Python modules

- Navigate to the project `part0/getting_started_python` directory in your terminal and run:

```
~/ai-for-developers/part0/getting_started_python % pip install -r requirements.txt
```

- Navigate to the project `part0/getting_started/client` directory in your terminal and run:

```
~/ai-for-developers/part0/client % npm install
```

4.  Launch the server

- In a terminal, navigate to the `part0/getting_started_python` directory and run the following command:

```
~/ai-for-developers/part0/getting_started_python % fastapi dev main.py
```

5.  Launch the client

- In a separate terminal, navigate to the `part0/client` directory and run the following commands:

```
~/ai-for-developers/part0/client % npm run dev
```

6. Open your web browser and visit: http://localhost:5173

7. Input a question and click `Call your API` to see the response streamed from Llama 3.2