# The Developer's Guide to AI - From Prompts to Agents

This repository contains the code for the book **The Developer's Guide to AI - From Prompts to Agents**.

The book is meant to be a comprehensive guide that makes AI approachable for developers. This book is designed to jumpstart your AI learning journey. No need for advanced Python, neural network training, or a PhD in statistics. All you need is basic JavaScript knowledge and a willingness to learn.

We focus on practical applications using pre-trained AI models (LLMs and more) through accessible APIs and SDKs, allowing you to build AI-powered applications in the languages you already know.

# Table of Contents

* [Part 1: Getting started with AI](part1/README.md)
	+ [Section 1: Getting Started](part1/getting_started/README.md)
	+ [Section 2: Simple RAG Example](part1/simple_rag_example/README.md)
* [Part 2: Prompt Engineering](part2/README.md)
	+ [Section 1: First Call Chain](part2/first_call_chain/README.md)
	+ [Section 2: Basic Examples](part2/basic_examples/README.md)
	+ [Section 3: Structured Output](part2/structured_output/README.md)
* [Part 3: Vector Databases and RAG](part3/README.md)
	+ [Section 1: Conversational RAG Example](part3/conversational_rag_example/README.md)
	+ [Section 2: Vector Databases](part3/vector_databases/README.md)
* [Part 4: Fine-tuning](part4/README.md)
	+ [Section 1: Model Development Notebooks](part4/README.md)
	+ [Section 2: Data Management](part4/data/README.md)
* [Part 5: Agents](part5/README.md)
	+ [Section 1: Hello Agents](part5/01-helloAgents.py)
	+ [Section 2: Finding Earnings Report](part5/02.findingEarningsReport.py)
	+ [Section 3: Multi-Agent Collaboration Platform](part5/mcp/README.md)


# Prerequisites

- Basic knowledge of JavaScript
- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)

# Project Structure

The project is organized into parts. Each part corresponds to a part with in book **The Developer's Guide to AI - From Prompts to Agents**.

- `part1/`: Getting started with AI
- `part2/`: Prompt Engineering
- `part3/`: Vector Databases and RAG
- `part4/`: Fine-tuning
- `part5/`: Agents

# Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/developers-guide-to-ai.git
   cd developers-guide-to-ai
   ```

2. Install dependencies for a specific part (example for part1):
   ```bash
   cd part1/getting_started/section1
   npm install
   ```

3. Follow the instructions in each part's README.md for specific setup and execution steps.

# Parts Overview

## Part 1: Getting started with AI
This part provides the foundation for working with AI, featuring both JavaScript and Python implementations.

### Getting Started

| Section | Description |
| --- | --- |
| [part1/getting_started/section1/](part1/getting_started/section1/) | REST service with Express and Node.js that interfaces with local LLMs using LangChain. Demonstrates basic LLM interaction through a simple API endpoint. |
| [part1/getting_started/section2/](part1/getting_started/section2/) | Implements real-time streaming of LLM responses using Express and LangChain. Shows how to create responsive UIs by sending text chunks as they're generated, similar to ChatGPT's typing effect. |
| [part1/client/](part1/client/) | A modern React-based frontend application that demonstrates how to consume the LLM API. Includes examples of handling streaming responses and managing UI states during generation. |

### Python Implementation
| Section | Description |
| --- | --- |
| [part1/getting_started_python/](part1/getting_started_python/) | A FastAPI-based alternative to the JavaScript implementation, showcasing Python's async capabilities for LLM interactions. Includes streaming support and demonstrates how to integrate with the same LLM backend using Python's ecosystem. |
| [part1/getting_started_python/rag/](part1/getting_started_python/rag/) | A Python implementation of Retrieval-Augmented Generation that shows how to enhance LLM responses with external knowledge sources, including document loading and retrieval mechanisms. |

---

## Part 2: Prompt Engineering
Dives deeper into LLM capabilities with practical examples and implementations.

| Section | Description |
| --- | --- |
| [part2/basic_examples/](part2/basic_examples/) | Comprehensive examples covering core LLM operations including prompt engineering, temperature settings, and response formatting. Includes practical patterns for different types of LLM interactions. |
| [part2/basic_examples_javascript/](part2/basic_examples_javascript/) | Web-focused implementations demonstrating how to integrate LLM capabilities into browser-based applications. Covers API integration, error handling, and response processing in a JavaScript environment. |
| [part2/first_call_chain/](part2/first_call_chain/) | A step-by-step guide to creating multi-step LLM workflows. Shows how to combine multiple LLM calls to solve complex tasks while maintaining context between interactions. |
| [part2/structured_output/](part2/structured_output/) | Techniques for extracting consistent, well-formatted data from LLM responses. Includes schema validation, output formatting, and error handling for production-grade applications. |

---

## Part 3: Vector Databases and RAG
Focuses on creating sophisticated AI applications with advanced RAG and vector database integrations.

| Section | Description |
| --- | --- |
| [part3/advanced_rag/](part3/advanced_rag/) | Implements cutting-edge Retrieval-Augmented Generation techniques including hybrid search, query expansion, and result re-ranking. Demonstrates how to improve answer quality and relevance. |
| [part3/conversational_rag_example/](part3/conversational_rag_example/) | Shows how to build context-aware chat applications that maintain conversation history. Implements memory mechanisms for coherent multi-turn interactions. |
| [part3/parent_document_retriever_rag/](part3/parent_document_retriever_rag/) | Advanced document processing pipeline that handles large documents through smart chunking and hierarchical retrieval. Ideal for processing PDFs, research papers, and technical documentation. |
| [part3/vector_databases/](part3/vector_databases/) | A guide to implementing vector similarity search. Covers embedding generation, indexing strategies, and performance optimization for large-scale retrieval. |
| [part3/simple_rag_javascript/](part3/simple_rag_javascript/) | A complete JavaScript implementation of RAG, demonstrating how to build end-to-end retrieval systems in the browser or Node.js environment. |

---

## Part 4: Fine-tuning
A comprehensive guide to taking LLMs from development to production, covering the entire machine learning lifecycle.

| Section | Description |
| --- | --- |
| [part4/01-dataset.ipynb](part4/01-dataset.ipynb) | Data preparation and exploration techniques for LLM fine-tuning, including data cleaning, normalization, and feature engineering |
| [part4/02.zeroShot.ipynb](part4/02.zeroShot.ipynb) | Implementing and evaluating zero-shot learning capabilities with pre-trained models |
| [part4/03-finetune-classificationModel.ipynb](part4/03-finetune-classificationModel.ipynb) | Fine-tuning strategies for classification tasks with performance optimization |
| [part4/04-chat-examples.ipynb](part4/04-chat-examples.ipynb) | Building production-ready chat interfaces with context management |
| [part4/05-finetune-dataset.ipynb](part4/05-finetune-dataset.ipynb) | Advanced dataset preparation, including data augmentation and balancing |
| [part4/06-finetune-llm.ipynb](part4/06-finetune-llm.ipynb) | End-to-end LLM fine-tuning pipeline with best practices |
| [part4/07-test-ft-llm.ipynb](part4/07-test-ft-llm.ipynb) | Comprehensive model evaluation, testing, and validation |

### Datasets
| Section | Description |
| --- | --- |
| [part4/data/](part4/data/) | Curated datasets for training and evaluation, including train/validation/test splits |
| [part4/rawData/](part4/rawData/) | Raw data processing and cleaning utilities for handling unstructured data |

---

## Part 5: Agents
Explores the frontier of AI with autonomous agent systems and multi-agent collaboration.

| Section | Description |
| --- | --- |
| [part5/01-helloAgents.py](part5/01-helloAgents.py) | Introduction to agent architectures and design patterns |
| [part5/02.findingEarningsReport.py](part5/02.findingEarningsReport.py) | Specialized financial data agent implementation |
| [part5/mcp/](part5/mcp/) | Multi-agent Collaboration Platform |

