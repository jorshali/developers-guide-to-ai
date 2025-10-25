from messages import ChatRequest
from conversation_history_example_data import conversation_history

chat_request = ChatRequest(
  question="What was I talking about?",
  history=conversation_history
)

print(chat_request.model_dump_json(indent=2))
