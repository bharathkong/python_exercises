import logging
import time
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


# -----------------------------------------------------
# Logging Configuration
# -----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

DOCUMENT_FOLDER = "./documents"
COLLECTION_NAME = "RefundsStore1"
QDRANT_URL = "http://localhost:6333"


total_start = time.perf_counter()


# -----------------------------------------------------
# 1. Load documents
# -----------------------------------------------------

logger.info("Starting document loading...")

start = time.perf_counter()

documents = []

for file_path in Path(DOCUMENT_FOLDER).glob("*.txt"):

    content = file_path.read_text(encoding="utf-8")

    document = Document(
        page_content=content,
        metadata={
            "source": file_path.name
        }
    )

    documents.append(document)

elapsed = time.perf_counter() - start

logger.info("Documents loaded: %d", len(documents))
logger.info("Document loading time: %.2f seconds", elapsed)


# -----------------------------------------------------
# 2. Split documents
# -----------------------------------------------------

logger.info("Starting document chunking...")

start = time.perf_counter()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

elapsed = time.perf_counter() - start

logger.info("Chunks created: %d", len(chunks))
logger.info("Chunking time: %.2f seconds", elapsed)


# -----------------------------------------------------
# 3. Create embedding model
# -----------------------------------------------------

logger.info("Initializing embedding model...")

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)


# -----------------------------------------------------
# 4. Store embeddings in Qdrant
# -----------------------------------------------------

logger.info("Starting Qdrant ingestion...")
logger.info("Number of chunks to ingest: %d", len(chunks))

start = time.perf_counter()

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=QDRANT_URL,
    collection_name=COLLECTION_NAME
)

ingestion_time = time.perf_counter() - start

logger.info(
    "Qdrant ingestion completed in %.2f seconds",
    ingestion_time
)


# -----------------------------------------------------
# 5. Check Qdrant count
# -----------------------------------------------------

qdrant_client = QdrantClient(
    url=QDRANT_URL
)

collection_info = qdrant_client.get_collection(
    COLLECTION_NAME
)

logger.info(
    "Total vectors in Qdrant: %d",
    collection_info.points_count
)


# -----------------------------------------------------
# 6. Total processing time
# -----------------------------------------------------

total_time = time.perf_counter() - total_start

logger.info("----------------------------------------")
logger.info("INGESTION SUMMARY")
logger.info("----------------------------------------")
logger.info("Documents       : %d", len(documents))
logger.info("Chunks          : %d", len(chunks))
logger.info("Qdrant vectors  : %d", collection_info.points_count)
logger.info("Ingestion time  : %.2f seconds", ingestion_time)
logger.info("Total time      : %.2f seconds", total_time)

if ingestion_time > 0:
    logger.info(
        "Throughput      : %.2f chunks/second",
        len(chunks) / ingestion_time
    )

logger.info("----------------------------------------")