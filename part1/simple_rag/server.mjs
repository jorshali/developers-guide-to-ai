import express from "express";
import cors from "cors";

import { DirectoryLoader } from "langchain/document_loaders/fs/directory";
import { TextLoader } from "langchain/document_loaders/fs/text";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { OllamaEmbeddings } from "@langchain/ollama";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { ParentDocumentRetriever } from "langchain/retrievers/parent_document";
import { InMemoryStore } from "@langchain/core/stores";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { ChatOllama } from "@langchain/ollama";

import {
  RunnableLambda,
  RunnableMap,
  RunnablePassthrough,
} from "@langchain/core/runnables";

import { StringOutputParser } from "@langchain/core/output_parsers";

const loader = new DirectoryLoader(
  "../articles",
  {
    ".md": (path) => new TextLoader(path)
  }
);

const documentsForVectorStore = await loader.load();

const embeddings = new OllamaEmbeddings({
  model: "mxbai-embed-large",
  baseUrl: "http://localhost:11434",
});

const vectorStore = new MemoryVectorStore(embeddings);
const byteStore = new InMemoryStore();

const retriever = new ParentDocumentRetriever({
  vectorstore: vectorStore,
  byteStore: byteStore,
  childSplitter: new RecursiveCharacterTextSplitter({
    chunkOverlap: 0,
    chunkSize: 50,
  })
});

console.log("\nCreating embeddings and loading Vectore Store, please be patient...")

await retriever.addDocuments(documentsForVectorStore)

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const chatModel = new ChatOllama({
  model: "llama3.2"
});

app.post("/", async (request, response) => {
  const { question } = request.body;

  console.log("\nReceived question: " + question);

  const prompt = ChatPromptTemplate.fromMessages([
    [
      "system",
      "Answer the question with company information based on only the following context:\n\n{context}"
    ],
    ["user", "{question}"]
  ]);

  const setupAndRetrieval = RunnableMap.from({
    context: new RunnableLambda({
      func: (input) =>
        retriever.invoke(input).then(
          (response) => {
            console.log("\nRelated article retrieved:\n");
            console.log("\n" + response[0].pageContent);
            console.log("\nCalling the LLM with context...");
            
            return response[0].pageContent;
          }),
    }).withConfig({ runName: "contextRetriever" }),
    question: new RunnablePassthrough(),
  });

  const outputParser = new StringOutputParser();

  const chain = setupAndRetrieval.pipe(prompt)
    .pipe(chatModel)
    .pipe(outputParser);
  
  const stream = await chain.stream(question);

  console.log("\nLLM response started, generating response chunks...")

  for await (const chunk of stream) {
    if (chunk) {
      response.write(chunk);
    }
  }

  console.log("\nResponse generation complete.");

  response.end();
});

app.listen(8000, () => {
  console.log("Server is running on port 8000");
});