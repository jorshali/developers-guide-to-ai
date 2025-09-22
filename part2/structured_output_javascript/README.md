# Data Extraction with Instructor.js and Zod

This JavaScript implementation provides the same functionality as the Python version using Instructor.js and Zod for structured output.

## Features

- **Structured Output**: Uses Zod schemas to define the expected output structure
- **Email Contact Extraction**: Extracts sender information from email content
- **OpenAI Integration**: Works with local Ollama instance via OpenAI-compatible API
- **Type Safety**: Zod provides runtime validation and type safety

## Prerequisites

- Node.js (version 18 or higher)
- Ollama running locally on port 11434
- Llama3.2 model available in Ollama

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

## Dependencies

- `instructor`: JavaScript library for structured output with LLMs
- `zod`: TypeScript-first schema validation library

## How it works

1. **Schema Definition**: Uses Zod to define the `ContactInformation` schema with optional fields
2. **Client Setup**: Configures Instructor.js client to work with local Ollama instance
3. **Extraction Function**: `extractContactInformation()` function processes emails and returns structured data
4. **Validation**: Zod automatically validates the LLM output against the defined schema

## Example Output

The script will extract and display contact information from two sample emails, showing:
- Sender name
- Location
- Job title
- Company
- Email address
- Phone number

## Comparison with Python Version

| Feature | Python (Pydantic) | JavaScript (Zod) |
|---------|-------------------|------------------|
| Schema Definition | `BaseModel` class | `z.object()` |
| Field Validation | `Field()` with descriptions | `z.string().describe()` |
| Email Validation | `EmailStr` | `z.string().email()` |
| Optional Fields | `Optional[str]` | `z.string().optional()` |
| JSON Schema | `model_json_schema()` | Direct schema object |
