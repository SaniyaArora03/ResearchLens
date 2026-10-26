from rag_test import load_papers
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


documents = load_papers()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"Total chunks: {len(chunks)}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

sample_text = chunks[0].page_content

vector = embeddings.embed_query(sample_text)

print("\nVector dimensions:", len(vector))
print("\nFirst 10 vector values:", vector[:10])