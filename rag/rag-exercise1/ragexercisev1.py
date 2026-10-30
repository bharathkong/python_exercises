
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from qdrant_client import QdrantClient


# 1. Load your actual documents
documents = [
    Document(
        page_content="Refunds are permitted within 30 days.",
        metadata={"source": "refund-policy.txt"}
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

retriever = vector_store.as_retriever()

results = retriever.invoke(question);

# pass the retrieved content to an LLM:
for doc in results:
    print(doc.page_content)
    

llm = ChatOllama(model="qwen2.5:3b")

prompt = ChatPromptTemplate.from_template("""
Answer the question using only the context.

Context:
{context}

Question:
{question}
""")

chain = (prompt | llm | StrOutputParser() )

response = chain.invoke({
    "context": "\n".join([doc.page_content for doc in results]),
    "question": question
})

print(response)