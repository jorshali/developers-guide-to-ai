import express from "express";
import { ChatOllama } from "@langchain/ollama";

const app = express();

const model = new ChatOllama({
  model: 'llama3.2'
});

app.get('/', async (request, response) => {
  response.type('text/plain');

  const modelResponse = 
    await model.invoke(
      "Can you simply say 'test'?");

  console.log("\nAIMessage object response:\n")
  console.log(modelResponse);

  response.send(modelResponse.content);
});

app.listen(8000, () => {
  console.log(`Server is running on port 8000`);
});