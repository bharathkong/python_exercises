import time
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from filereadservice import *
from utilities import *

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------


# -----------------------------------------------------
# Logging
# -----------------------------------------------------

collection_name = get_collectionname()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------------------------------
# 1. Connect to Qdrant
# -----------------------------------------------------

qdrant_client = get_qdrantclient()


# -----------------------------------------------------
# 2. Create embedding model
# -----------------------------------------------------

embedding_model = get_embedding_model()


# -----------------------------------------------------
# 3. Create collection if it doesn't exist
# -----------------------------------------------------

createcollection()

# -----------------------------------------------------
# 4. Connect LangChain to collection
# -----------------------------------------------------

vector_store =get_vectorstore()


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
    collection_name
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
