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


message = "Based on Amazon's Q4 2024 earnings report, what is the revenue for the quarter?"
message = "Based on Google's Q4 2024 earnings report, what is the revenue for the quarter?"
message = "Based on Apple's Q4 2024 earnings report, what is the revenue for the quarter?"
# message = "In a table, show net sales, operating income, net income and EPS of Amazon, Google and Apple for Q4 2024"

message = "You are a financial analyst. You need to find the earnings report for Amazon, Google and Apple for Q4 2024. From the earnings report, you need find the revenue for each company and compare them in a table."

message = "Show me the Q4 2024 revenue for Amazon, Google and Apple and compare them in a table."
message = "Show me the Q4 2024 revenue and EPS for Amazon, Google and Apple and compare them in a table."
agent.run(message)
