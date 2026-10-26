
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


VECTOR_STORE_DIR = (
    Path(__file__).resolve().parent.parent / "vector_store"
)


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    
    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store


if __name__ == "__main__":
    vector_store = load_vector_store()

    query = input("\nAsk a question about your research papers: ")

    results = vector_store.similarity_search_with_score(
        query,
        k=3
    )

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\n--- Result {i} | Distance: {score:.4f} ---")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Page: {doc.metadata.get('page', 'Unknown')}")
        print(doc.page_content[:700])
