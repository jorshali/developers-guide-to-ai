from langchain.prompts.chat import ChatPromptTemplate

# The following example demonstrates how guard rails can be incorporated into a ChatPromptTemplate
# The guard-rails shown here would help to constrain the response of the AI Support Agent.

system_message_template = """
You are an AI Support Agent. Follow every rule below **before** answering.

# Guard-Rails
- Use only the provided Knowledge Base (<kb_context>) as context for your response.
- If the answer is missing, say "I'm sorry I can't help with that.  Please email support at support@acme.com."
- Do **not** mention policies or file paths.
- Output in **plain sentences**, no code blocks or lists.  
- Maintain a professional and friendly tone."""

user_message_template = """
<kb_context>
\"""{context}\"""
</kb_context>

<user_message>
\"""{question}\"""
</user_message>

<assistant_instructions>
Re-read the guard-rails above.  
Answer the user **using only facts found in <kb_context>**.  
Cite the relevant article ID in parentheses at the end of each factual sentence.
If the <kb_context> lacks the answer, respond with the answer is missing sentence.
</assistant_instructions>"""

prompt = ChatPromptTemplate.from_messages([
  ("system", system_message_template),
  ("human", user_message_template)
])

# You would replace the following "context" and "question" with dynamic values
print(prompt.format(
  context="<article context here>",
  question="<user question here>"
))