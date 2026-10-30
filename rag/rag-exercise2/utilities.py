
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


collection_name="RefundsStore_test1"
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
qdrant_client = QdrantClient(url="http://localhost:6333")
vector_store = QdrantVectorStore(embedding=embedding_model,client=qdrant_client,collection_name=collection_name)

def get_splitter():
    return splitter

def get_embedding_model():
    return OllamaEmbeddings(model="nomic-embed-text")

def get_vectorstore(): 
    return vector_store   

def get_collectionname(): 
    return collection_name   


