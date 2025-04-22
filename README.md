# The Developers Guide to AI - From Prompts to Agents (coming soon)

Finally, a book that makes AI approachable for developers.  This book is here to jumpstart your AI learning journey.  You won’t need to dust off your Python spellbook, train neural networks, or get a PhD in statistics.  All you need is some basic JavaScript knowledge and a willingness to learn.

We’ll skip all the data science wizardry by using pretrained AI models (LLMs and more).  APIs and SDKs have made these models accessible to developers in the languages they’re already building applications with.

This book will guide you through techniques to combine your own data with the power of LLMs. During this journey, you'll learn important concepts while gaining practical experience.

## Project Structure

The project contains folders with examples to support "The Developer's Guide to AI" boook.  Each folder contains the example for that part in the series.  All examples will use [Ollama](https://ollama.com) to connect to a local LLM.

### Part 0: Setting the Stage

#### Getting Started

Most developers are familiar with JavaScript.  This chapter shows how quickly you can call a local LLM from a UI with the following JavaScript technologies:

- [React](https://react.dev)
- [Vite](https://vite.dev)
- [Node.js](https://nodejs.org/docs/latest/api/)
- [Express](https://expressjs.com/en/4x/api.html)
- [LangChain.js](https://js.langchain.com/docs/get_started/introduction)

Example code:

- [part1/getting_started/section1](part1/getting_started/section1): Build a REST Service that calls a local LLM
- [part1/getting_started/section2](part1/getting_started/section2): Stream your LLM Responses

#### Building a RAG Solution

We'll take our JavaScript solution further by building a simple RAG solution.  We'll add an in-memory Vector Database and combine it with our LLM using some additional LangChain components.

Example code:

- [part1/simple_rag](part1/simple_rag): RAG solution with a Vector Store and local LLM

For each part you'll find a `README.md` with instructions to get the example up and running.
