# This file tests the RAG (Retrieval-Augmented Generation) pipeline's query processing.
# It ensures that the get_qa_chain function correctly processes a user query and retrieves relevant context,
# with the result containing the expected answer to the question (e.g., "What is mental health?").

from dotenv import load_dotenv
load_dotenv()

from app.core.rag_chain import get_qa_chain

def test_qa_chain():
    qa_chain = get_qa_chain()
    response = qa_chain.invoke({"query": "What is mental health?"})
    print("QA Response:", response)
    assert "mental health" in response["result"].lower()
