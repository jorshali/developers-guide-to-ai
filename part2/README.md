# The Developer's Guide to AI - From Prompts to Agents

## Introduction

The `part2` examples dive deeper into LLM capabilities with practical examples of prompt engineering techniques.

## Quick Start

The following steps will get you up and running on your machine.

0. Install Ollama and run:

- Download and install: https://ollama.com
- Verify the install and start Llama in a terminal window:

```
~ % ollama run llama3.2
```

1. Install Python (if necessary)

It's recommended that you setup a virtual environment before installing Python or Python modules.  You can see how to do that here:

[Python Virtual Environment](https://github.com/jorshali/developers-guide-to-ai/blob/main/README.md#virtual-environment-setup)

If you would rather install Python globally, follow the instructions here:

- Download and install: https://www.python.org/downloads/
- Verify the install in your terminal:

```
~ % python -V
```

- If the installation succeeded, the version will print

2. Install Python modules

- Navigate to the project (e.g. `part2/basic_examples`) directory in your terminal and run:

```
~/developers-guide-to-ai/part2/basic_examples % pip install -r requirements.txt
```

3.  Run a Python script

- In a terminal, navigate to the project directory (e.g. `part2/basic_examples`) and run the following command:

```
~/developers-guide-to-ai/part2/basic_examples % python tokenization.py
```

If the instructions differ (e.g. `part2/first_call_chain`) a specific `README` file will be provided.