import { CharacterTextSplitter } from "langchain/text_splitter";

async function splitArticle(text) {
  const splitter = new CharacterTextSplitter({
    separator: "",
    chunkSize: 70,
    chunkOverlap: 20
  });
  
  const output = await splitter.splitText(text);

  console.log(output);
}

const text = "Our system requires multi-factor Authentication (MFA). " +
  "This helps to keep your account secure.  This step-by-step guide will " +
  "walk you through the setup."

splitArticle(text);