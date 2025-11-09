import express from "express";
import { Ollama } from "ollama";
import cors from 'cors';

const app = express();

app.use(cors());
app.use(express.json());

const ollama = new Ollama();

app.post('/', async (request, response) => {
  response.type('text/plain');

  const body = request.body;

  const streamIterator = await ollama.generate({
    model: 'llama3.2',
    prompt: body.question,
    stream: true
  });

  for await (const chunk of streamIterator) {
    response.write(chunk.response);
  }

  response.end();
});

app.listen(8000, () => {
  console.log(`Server is running on port 8000`);
});