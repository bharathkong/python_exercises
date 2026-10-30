
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from qdrant_client import QdrantClient
from ollama import chat
from utilities import *

# 4. Retrieve relevant chunks




def main():
    question = input("Can you ask question?  ")
    retrieved_docs = get_vectorstore().similarity_search(question, k=10)
    print("Retrived doc count is : " , len(retrieved_docs))
    #for doc in retrieved_docs:
    #    print(doc.page_content)
    
        
        # Build context  only with top 5 documents  
    context = "\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    # Build Messaged
    messages = [
    {
        "role": "system",
        "content": """
        Answer only from the provided context.
        If the answer is unavailable, say so.
        """
    },
    {
        "role": "user",
        "content": f"""
        Context:
        {context}

        Question:
        {question}
        """
    }
    ]
    # Call ollama 
    response = chat(
        model="qwen2.5:3b",
        messages=messages
    )

    print(response.message.content)
    
if __name__ == "__main__":
    main()
