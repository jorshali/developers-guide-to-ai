# Building an MCP Server

This directory contains examples for building a Multi-Client Protocol (MCP) server.

## Folders and Files
- `mongo-client.py`: MongoDB client for managing expenses.
- `myExpenseManager-mcp-client.py`: MCP client for the expense manager server.
- `myExpenseManager-mcp-server.py`: MCP server for the expense manager.
- `mySpecialCalculator-mcp-server.py`: MCP server for a special calculator.
- `requirements.txt`: Python dependencies for this project.

# Setting up the environment

To set up the environment, you can use `pyenv` and `pyenv-virtualenv` to create a virtual environment for the project. After setting up the virtual environment, you can install the required packages using `pip install -r requirements.txt`.

Once you have set up the virtual environment and installed the required packages, you can activate the virtual environment.

For example, to set up the virtual environment, you can use the following commands:

```bash
pyenv virtualenv 3.12.0 developers-guide-to-ai-part5-mcp-server
pyenv activate developers-guide-to-ai-part5-mcp-server
pip install -r requirements.txt
```