
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from qdrant_client import QdrantClient
from ollama import chat

collection_name="RefundsStore1"

# 1. Load your actual documents
documents = [
    Document(
        page_content="Refunds are permitted within 30 days.",
        metadata={"source": "refund-policy.txt"}
    ), 
    
    Document(
        page_content="Refunds are applicable only for long term employees.",
        metadata={"source": "refund-policy-01.txt"}
    ),

    Document(
        page_content="Customers can request a full refund within 7 days of purchase.",
        metadata={"source": "refund-policy-02.txt"}
    ),

    Document(
        page_content="Refund requests submitted after 30 days will not be accepted.",
        metadata={"source": "refund-policy-03.txt"}
    ),

    Document(
        page_content="Subscription charges are refundable during the first 14 days.",
        metadata={"source": "refund-policy-04.txt"}
    ),

    Document(
        page_content="Digital products are non-refundable once downloaded.",
        metadata={"source": "refund-policy-05.txt"}
    ),

    Document(
        page_content="Refunds for damaged products require proof of purchase.",
        metadata={"source": "refund-policy-06.txt"}
    ),

    Document(
        page_content="Customers are eligible for a partial refund if the service was used.",
        metadata={"source": "refund-policy-07.txt"}
    ),

    Document(
        page_content="Event ticket purchases are refundable up to 48 hours before the event.",
        metadata={"source": "refund-policy-08.txt"}
    ),

    Document(
        page_content="Refunds are processed within 10 business days of approval.",
        metadata={"source": "refund-policy-09.txt"}
    ),

    Document(
        page_content="Refund requests must be submitted through the customer portal.",
        metadata={"source": "refund-policy-10.txt"}
    ),

    Document(
        page_content="Products purchased during clearance sales are not eligible for refunds.",
        metadata={"source": "refund-policy-11.txt"}
    ),

    Document(
        page_content="Students may request a course refund within the first week of enrollment.",
        metadata={"source": "refund-policy-12.txt"}
    ),

    Document(
        page_content="Refunds are not granted for services already completed.",
        metadata={"source": "refund-policy-13.txt"}
    ),

    Document(
        page_content="A cancellation fee may be deducted from the refunded amount.",
        metadata={"source": "refund-policy-14.txt"}
    ),

    Document(
        page_content="Refund eligibility depends on compliance with warranty conditions.",
        metadata={"source": "refund-policy-15.txt"}
    ),

    Document(
        page_content="Customers can exchange products instead of requesting a refund.",
        metadata={"source": "refund-policy-16.txt"}
    ),

    Document(
        page_content="Membership fees are refundable only under exceptional circumstances.",
        metadata={"source": "refund-policy-17.txt"}
    ),

    Document(
        page_content="Refunds for duplicate payments will be issued automatically.",
        metadata={"source": "refund-policy-18.txt"}
    ),

    Document(
        page_content="Corporate clients must submit refund requests through their account manager.",
        metadata={"source": "refund-policy-19.txt"}
    ),

    Document(
        page_content="Refunds are available when orders cannot be fulfilled by the supplier.",
        metadata={"source": "refund-policy-20.txt"}
    ),

    Document(
        page_content="Travel booking refunds are subject to airline cancellation policies.",
        metadata={"source": "refund-policy-21.txt"}
    ),

    Document(
        page_content="Refund requests require a valid transaction reference number.",
        metadata={"source": "refund-policy-22.txt"}
    ),

    Document(
        page_content="Customers who receive defective products can claim a full refund.",
        metadata={"source": "refund-policy-23.txt"}
    ),

    Document(
        page_content="Refunds for annual subscriptions are prorated based on usage.",
        metadata={"source": "refund-policy-24.txt"}
    ),

    Document(
        page_content="Gift card purchases are non-refundable and non-transferable.",
        metadata={"source": "refund-policy-25.txt"}
    ),

    Document(
        page_content="Refunds may be denied if misuse of the product is detected.",
        metadata={"source": "refund-policy-26.txt"}
    ),

    Document(
        page_content="Customers can track refund status from the order history page.",
        metadata={"source": "refund-policy-27.txt"}
    ),

    Document(
        page_content="Refunds for canceled training programs are processed within 15 days.",
        metadata={"source": "refund-policy-28.txt"}
    ),

    Document(
        page_content="Orders shipped internationally may incur non-refundable customs charges.",
        metadata={"source": "refund-policy-29.txt"}
    ),

    Document(
        page_content="A refund can be requested if delivery exceeds 30 days beyond the promised date.",
        metadata={"source": "refund-policy-30.txt"}
    ),

    Document(
        page_content="Refunds are issued to the original payment method used during purchase.",
        metadata={"source": "refund-policy-31.txt"}
    ),

    Document(
        page_content="Customers must return products in their original packaging for a refund.",
        metadata={"source": "refund-policy-32.txt"}
    ),

    Document(
        page_content="Refunds for online workshops are available before the first session begins.",
        metadata={"source": "refund-policy-33.txt"}
    ),

    Document(
        page_content="Refund requests are reviewed within three business days.",
        metadata={"source": "refund-policy-34.txt"}
    ),

    Document(
        page_content="Premium support fees are not refundable after activation.",
        metadata={"source": "refund-policy-35.txt"}
    ),

    Document(
        page_content="A refund will be issued when an order is canceled by the company.",
        metadata={"source": "refund-policy-36.txt"}
    ),

    Document(
        page_content="Customers can appeal a rejected refund request within 14 days.",
        metadata={"source": "refund-policy-37.txt"}
    ),

    Document(
        page_content="Refunds are not available for promotional giveaway items.",
        metadata={"source": "refund-policy-38.txt"}
    ),

    Document(
        page_content="Pre-order payments are refundable until the product release date.",
        metadata={"source": "refund-policy-39.txt"}
    ),

    Document(
        page_content="Approved refunds will trigger an email confirmation notification.",
        metadata={"source": "refund-policy-40.txt"}
    ),
      Document(
            page_content="Refunds are applicable only for long term employees.",
            metadata={"source": "refund-policy.txt"}
        ),
         Document(
            page_content="java is object oriented technolgoy.",
            metadata={"source": "java-tech.txt"}
        ),
         Document(
            page_content="javascript is easy language to code .",
            metadata={"source": "java-script-tech.txt"}
        ),
         Document(
            page_content="Python in the best and quick learning language .",
            metadata={"source": "python-tech.txt"}
        ),
         Document(
            page_content="World is beautiful .",
            metadata={"source": "world.txt"}
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
    collection_name=collection_name
)

collection_info = qdrant_client.get_collection(collection_name)
print("Total documents added in Qdrant Vector store is ", collection_info.points_count)
    
