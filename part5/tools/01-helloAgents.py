from smolagents import CodeAgent, LiteLLMModel
from smolagents import DuckDuckGoSearchTool, VisitWebpageTool

model_id = "gemini/gemini-2.0-flash"

model = LiteLLMModel(
    model_id=model_id,
    provider="google",
)

tools = [
    DuckDuckGoSearchTool(),
    VisitWebpageTool()
]

agent = CodeAgent(
    tools=tools,
    model=model,
    add_base_tools=True,
    verbosity_level=2,
    max_steps=5
)


message = "Based on Amazon's Q4 2024 earnings report, what is the revenue for the quarter?"
agent.run(message)
