import express from "express";
import { Ollama } from "ollama";

const app = express();

const model = new Ollama();

app.get('/', async (request, response) => {
  response.type('text/plain');

  const modelResponse = await model.generate({
    prompt: "Can you simply say 'test'?",
    model: 'llama3.2'
  });

  console.log("\nAIMessage object response:\n")
  console.log(modelResponse);

  response.send(modelResponse.response);
});

app.listen(8000, () => {
  console.log(`Server is running on port 8000`);
});