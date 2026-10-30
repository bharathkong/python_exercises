
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import logging
from qdrant_client.models import Distance, VectorParams



QDRANT_URL = "http://localhost:6333"
collection_name = "RefundsStore1"
BATCH_SIZE = 15
logger = logging.getLogger(__name__)

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
qdrant_client = QdrantClient(QDRANT_URL)
#vector_store = QdrantVectorStore(embedding=embedding_model,client=qdrant_client,collection_name=collection_name)

def get_splitter():
    return splitter

def get_embedding_model():
    return OllamaEmbeddings(model="nomic-embed-text")


def get_collectionname(): 
    return collection_name

def get_qdrantclient(): 
    return qdrant_client     

def get_vectorstore():
    
    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        collection_name=collection_name,
        url=QDRANT_URL
    )
    return vector_store

def createcollection():
    if not qdrant_client.collection_exists(collection_name):

        logger.info("Collection does not exist. Creating %s...", collection_name)

        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

        logger.info("Collection created successfully.")

    else:
        
        logger.info(
            "Collection %s already exists.",
            collection_name
        )

    