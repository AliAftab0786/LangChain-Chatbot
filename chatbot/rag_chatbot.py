import os
import json
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def initialize_chatbot():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Get the absolute path to the products.json file and Chroma persistence directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    products_path = os.path.join(os.path.dirname(current_dir), "data", "products.json")
    persist_dir = os.path.join(os.path.dirname(current_dir), "data", "chroma_db")

    # Load scraped data
    with open(products_path, "r") as f:
        products = json.load(f)

    # Convert products to Documents for LangChain
    documents = [
        Document(
            page_content=f"Title: {p['title']}\nPrice: Rs {p['price']}\nRating: {p['rating']}",
            metadata={"title": p["title"]}
        )
        for p in products
    ]

    # Set up vector store with Hugging Face embeddings and persistence
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=persist_dir
    )
    vector_store.persist()

    # Initialize LLM (Claude)
    llm = ChatAnthropic(
        model="claude-3-sonnet-20240229",
        anthropic_api_key=api_key,
        temperature=0
    )

    # Define a prompt template using context and question
    prompt_template = """
    Based on the provided context, answer the following question. Start your response with:
    "Answer: According to the information provided, "
    and then provide the specific answer to the question. Do not add 'out of 5' or any rating scale unless explicitly asked.

    Context:
    {context}

    Question:
    {question}
    """
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Create RetrievalQA chain with custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,  # For debugging
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa_chain

# Global variable to hold the QA chain (initialized once)
qa_chain = initialize_chatbot()

def get_response(query):
    # Get the raw response from the QA chain
    result = qa_chain({"query": query})
    response = result["result"]
    # Post-process to ensure "out of 5" is removed (backup)
    if "out of 5" in response:
        response = response.replace("out of 5", "").rstrip(".")
    return response

if __name__ == "__main__":
    # Test the chatbot
    print(get_response("What’s the price of Storage Carry Case 27.5cm x 17.5cm x 26cm?"))
    print(get_response("Which products are under Rs 5,000?"))
    print(get_response("What’s the rating of Wooden Storage Box 35cm x 25cm x 17cm?"))