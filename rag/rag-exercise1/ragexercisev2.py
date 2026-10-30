
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from qdrant_client import QdrantClient
from ollama import chat

# 1. Load your actual documents
documents = [
    Document(
        page_content="Refunds are permitted within 30 days.",
        metadata={"source": "refund-policy.txt"}
    ),
      Document(
            page_content="Refunds are applicable only for long term employees.",
            metadata={"source": "refund-policy.txt"}
        ),
         Document(
            page_content="java is object oriented technolgoy.",
            metadata={"source": "java-tech.txt"}
        )
]


# 2. Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)


# 3. Create embeddings and vector index
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
qdrant_client = QdrantClient(url="http://localhost:6333")


#Store the data in Vector store
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    #client = qdrant_client,
    collection_name="epam_interview_rag"
)


# 4. Retrieve relevant chunks
question = "What is the period for refund?"
retrieved_docs = get_vectorstore().similarity_search(question, k=10)


# Build context    
context = "\n".join(
    [
        doc.page_content
        for doc in retrieved_docs
    ]
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

