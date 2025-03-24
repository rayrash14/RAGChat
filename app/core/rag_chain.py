from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.core.embedding import load_faiss_store
from app.core.llm import load_llm

# Custom prompt template for the question-answering chain
CUSTOM_PROMPT_TEMPLATE = """ 
Use the pieces of information in the context to answer users' question.
If you do not know the answer, just say that you do not know the answer.
If the question is outside of the context, say it lies outside of your expertise zone.

Context:
{context}

Question:
{question}

Start the answer directly. No small talk.
"""

# Function to return the custom prompt template with context and question variables
def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])

# Function to initialize and return the question-answering chain (QA chain)
def get_qa_chain():
    retriever = load_faiss_store().as_retriever(search_kwargs={"k": 2})  # Search for the top 2 results
    llm_fn = load_llm()  # Returns function: prompt -> output

    from langchain.chains import RetrievalQAWithSourcesChain
    from langchain.llms.base import LLM

    # Define a custom LLM class to use the Hugging Face inference for text generation
    class HFCustomLLM(LLM):
        def _call(self, prompt, stop=None):
            return llm_fn(prompt)

        @property
        def _llm_type(self):
            return "custom_hf_inference"
    
    # Create the QA chain using RetrievalQA with the custom LLM and FAISS retriever
    qa_chain = RetrievalQA.from_chain_type(
        llm=HFCustomLLM(),  # Use the custom LLM for text generation
        chain_type="stuff",  # Use the "stuff" chain type (combines documents into one context)
        retriever=retriever,  # Provide the retriever for document retrieval
        chain_type_kwargs={"prompt": set_custom_prompt()},  # Use the custom prompt for the QA chain
        return_source_documents=True  # Return the source documents that were used for generating the answer
    )
    return qa_chain
