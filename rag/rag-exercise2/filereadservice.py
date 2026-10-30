from pathlib import Path

from langchain_core.documents import Document



# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

DOCUMENT_FOLDER = "./documents"

# -----------------------------------------------------
# 1. Read files and create Documents
# -----------------------------------------------------

def getchunksfromfiles():
    documents = []

    for file_path in Path(DOCUMENT_FOLDER).glob("*.txt"):
        print("Reading file -> "+ file_path.name)
        content = file_path.read_text(encoding="utf-8")

        document = Document(
            page_content=content,
            metadata={
                "source": file_path.name
            }
        )

    documents.append(document)

    return documents;
