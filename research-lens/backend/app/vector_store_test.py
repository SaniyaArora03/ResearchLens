
from rag_test import load_papers
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


documents = load_papers()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)
print(f"\nTotal chunks: {len(chunks)}")


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

print("FAISS vector store created successfully!")


query = "What methods are used for disease prediction?"

results = vector_store.similarity_search_with_score(
    query,
    k=3
)

print(f"\nQuery: {query}")
print("\nTop 3 relevant passages:\n")

for i, (doc, score) in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print(f"Distance score: {score:.4f}")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
    print(f"Page: {doc.metadata.get('page', 'Unknown')}")
    print(f"Content:\n{doc.page_content[:700]}")
