from smolagents import CodeAgent, LiteLLMModel

model_id = "gemini/gemini-2.0-flash"

model = LiteLLMModel(
    model_id=model_id,
    provider="google",
)

tools = []

agent = CodeAgent(
    tools=tools,
    model=model,
    add_base_tools=True
)


message = "Show me the Q4 2024 revenue for Amazon, Google and Apple and compare them in a table."
agent.run(message)
