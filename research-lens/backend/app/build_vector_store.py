
from pathlib import Path

from rag_test import load_papers
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Location where the FAISS index will be saved
VECTOR_STORE_DIR = (
    Path(__file__).resolve().parent.parent / "vector_store"
)


def build_vector_store():
    # 1. Load research papers
    documents = load_papers()

    # 2. Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)

    print(f"\nTotal chunks: {len(chunks)}")

    # 3. Initialize embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 4. Build FAISS index
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # 5. Save index and document metadata
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(VECTOR_STORE_DIR))

    print(f"\nVector store saved to: {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    build_vector_store()
