import { encoding_for_model } from "tiktoken";

async function countTokens(text, modelName) {
  // all Open AI models are supported
  const encoding = encoding_for_model(modelName);

  // Tokenize the text
  const tokens = encoding.encode(text);

  console.log(tokens)
  console.log(`Number of tokens: ${tokens.length}`);

  // Cleanup
  encoding.free();
}

const modelName = "gpt-4o-mini";
const sampleText = "I'm having password issues, can you help me login?";

countTokens(sampleText, modelName);