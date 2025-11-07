import express from "express";
import { Ollama } from "ollama";

const app = express();

const ollama = new Ollama();

app.get('/', async (request, response) => {
  response.type('text/plain');

  const modelResponse = await ollama.generate({
    model: 'llama3.2',
    prompt: "Can you simply say 'test'?"
  });

  console.log("\nAIMessage object response:\n")
  console.log(modelResponse);

  response.send(modelResponse.response);
});

app.listen(8000, () => {
  console.log(`Server is running on port 8000`);
});