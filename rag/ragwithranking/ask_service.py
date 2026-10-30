
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
    pairs = [
    (
        question,
        doc.page_content
    )
    for doc in retrieved_docs
    ]
    
    scores = reranker.predict(pairs)
    re_ranked_documents = sorted(
        zip(retrieved_docs, scores),
        key=lambda x: x[1],
        reverse=True
    )
    print("Reranked document count is : " , len(re_ranked_documents))
        
    # Filter only top 5 reranked documents
    top_5_docs = re_ranked_documents[:5]
      
    print("Reranked and filtered  count is : " , len(top_5_docs))
        
        # Build context  only with top 5 documents  
    context = "\n".join(
        doc.page_content
        for doc, score in top_5_docs
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
