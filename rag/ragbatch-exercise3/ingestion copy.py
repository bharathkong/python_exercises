import time
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from filereadservice import *


# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "RefundsStore1"
BATCH_SIZE = 100


# -----------------------------------------------------
# Logging
# -----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------------------------------
# 1. Connect to Qdrant
# -----------------------------------------------------

qdrant_client = QdrantClient(
    url=QDRANT_URL
)


# -----------------------------------------------------
# 2. Create embedding model
# -----------------------------------------------------

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)


# -----------------------------------------------------
# 3. Create collection if it doesn't exist
# -----------------------------------------------------

if not qdrant_client.collection_exists(COLLECTION_NAME):

    logger.info("Collection does not exist. Creating %s...", COLLECTION_NAME)

    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        )
    )

    logger.info("Collection created successfully.")

else:

    logger.info(
        "Collection %s already exists.",
        COLLECTION_NAME
    )


# -----------------------------------------------------
# 4. Connect LangChain to collection
# -----------------------------------------------------

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=embedding_model
)


# -----------------------------------------------------
# 5. Batch ingestion
# -----------------------------------------------------

logger.info("Starting ingestion...")

total_start = time.perf_counter()

documents = getchunksfromfiles();
print ("Total documents size", len(documents))
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks= splitter.split_documents(documents)
for start_index in range(0, len(chunks), BATCH_SIZE):

    batch_start = time.perf_counter()

    batch = chunks[
        start_index:start_index + BATCH_SIZE
    ]

    vector_store.add_documents(
        documents=batch
    )

    batch_time = time.perf_counter() - batch_start

    processed = min(
        start_index + BATCH_SIZE,
        len(chunks)
    )

    logger.info(
        "Inserted %d/%d | Batch size=%d | Time=%.2f sec",
        processed,
        len(chunks),
        len(batch),
        batch_time
    )


# -----------------------------------------------------
# 6. Total ingestion time
# -----------------------------------------------------

total_time = time.perf_counter() - total_start


# -----------------------------------------------------
# 7. Check Qdrant count
# -----------------------------------------------------

collection_info = qdrant_client.get_collection(
    COLLECTION_NAME
)


logger.info("---------------------------------------")
logger.info("INGESTION SUMMARY")
logger.info("---------------------------------------")

logger.info(
    "Total chunks      : %d",
    len(chunks)
)

logger.info(
    "Vectors in Qdrant : %d",
    collection_info.points_count
)

logger.info(
    "Total time        : %.2f seconds",
    total_time
)

logger.info(
    "Throughput        : %.2f vectors/sec",
    len(chunks) / total_time
)

logger.info("---------------------------------------")
