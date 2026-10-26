
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.query_vector_store import load_vector_store


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing from your .env file")

# 1. Load the saved FAISS index
vector_store = load_vector_store()

# 2. Configure the language model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=api_key,
)

# 3. Define instructions for evidence-grounded answers
prompt = ChatPromptTemplate.from_template("""
You are ResearchLens, an assistant that helps users understand
research papers.

Answer the question using ONLY the context provided below.
If the context does not contain enough information, say so.
Do not invent findings, facts, or citations.

For every important claim, cite the source filename and page
number using the metadata supplied with each passage.

Context:
{context}

Question:
{question}
""")

# 4. Build the answer-generation chain
chain = prompt | llm | StrOutputParser()


def ask_question(question: str):
    # Retrieve relevant passages
    results = vector_store.similarity_search_with_score(
        question,
        k=4
    )

    # Attach source metadata to each passage
    context_parts = []

    for doc, score in results:
        source = os.path.basename(
            doc.metadata.get("source", "Unknown")
        )
        page = doc.metadata.get("page", "Unknown")

        context_parts.append(
            f"Source: {source}, page: {page}\n"
            f"Passage:\n{doc.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # Generate an answer from the retrieved evidence
    answer = chain.invoke({
        "context": context,
        "question": question
    })

    return answer


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.strip().lower() == "exit":
            break

        if question.strip():
            ask_question(question)
