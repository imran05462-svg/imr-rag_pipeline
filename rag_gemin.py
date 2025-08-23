import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

def main():
    """
    Main function to run the RAG application.
    """
    # 1. Load environment variables from .env file
    load_dotenv()
    print("Environment variables loaded successfully.")

    # 2. Load and Split Document
    print("Loading and splitting the document...")
    loader = PyPDFLoader("imr-sop.pdf") # Make sure this PDF is in the same folder
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    split_docs = text_splitter.split_documents(docs)
    print(f"Document split into {len(split_docs)} chunks.")

    # 3. Create Embeddings and Store in Pinecone
    print("Initializing models and Pinecone...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    index_name = "imrindex"

    print(f"Creating or connecting to Pinecone index: {index_name}")
    vectorstore = PineconeVectorStore.from_documents(
        split_docs,
        embedding=embeddings,
        index_name=index_name
    )
    print("Pinecone vector store is ready.")

    # 4. Build the RAG Chain
    template = """
    You are a helpful assistant. Answer the user's question based only on the following context.
    If the context does not contain the answer, state that you don't know.

    Context:
    {context}

    Question:
    {question}
    """
    prompt = PromptTemplate.from_template(template)

    # Initialize the Gemini chat model. The new library handles "gemini-pro" correctly.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.3)
    
    retriever = vectorstore.as_retriever()

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("RAG chain created.")

    # 5. Start the Q&A Loop
    print("\nRAG Q&A Ready! Type your question (or 'exit' to quit)\n")
    while True:
        user_q = input("Enter your question: ").strip()
        if user_q.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not user_q:
            continue

        print("\n" + "=" * 80)
        print("Q:", user_q)
        print("-" * 80)
        
        answer = rag_chain.invoke(user_q)
        print("A:", answer)
        
        print("=" * 80 + "\n")

if __name__ == "__main__":
    main()