import { OpenAIEmbeddings } from '@langchain/openai';

const embeddings = new OpenAIEmbeddings({
  modelName: 'text-embedding-3-small'
});

const result = await embeddings.embedQuery(
  'I’m having password issues, can you help login?');

console.log(result);