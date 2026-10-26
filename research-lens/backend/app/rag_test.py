from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader


PAPERS_DIR = Path(__file__).resolve().parent.parent / "data" / "papers"


def load_papers():
    documents = []

    for pdf_path in PAPERS_DIR.glob("*.pdf"):
        print(f"\nLoading: {pdf_path.name}")

        loader = PyMuPDFLoader(str(pdf_path))
        docs = loader.load()

        print(f"Pages loaded: {len(docs)}")

        documents.extend(docs)

    return documents


if __name__ == "__main__":
    documents = load_papers()

    print("\n==============================")
    print(f"Total pages loaded: {len(documents)}")
    print("==============================")

    if documents:
        first_doc = documents[0]

        print("\n--- FIRST PAGE CONTENT ---\n")
        print(first_doc.page_content[:2000])

        print("\n--- METADATA ---\n")
        print(first_doc.metadata)