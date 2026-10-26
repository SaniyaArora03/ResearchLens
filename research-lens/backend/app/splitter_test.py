from rag_test import load_papers
from langchain_text_splitters import RecursiveCharacterTextSplitter


documents = load_papers()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"\nOriginal documents: {len(documents)}")
print(f"Total chunks: {len(chunks)}")

print("\n--- FIRST CHUNK ---\n")
print(chunks[0].page_content)

print("\n--- FIRST CHUNK METADATA ---\n")
print(chunks[0].metadata)