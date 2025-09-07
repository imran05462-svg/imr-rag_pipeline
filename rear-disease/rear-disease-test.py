import os
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
import gradio as gr

def build_qa_chain():
    load_dotenv()
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    pinecone_key = os.getenv("PINECONE_API_KEY")
    rag_model = "guan-wang/ReDis-QA"
    embedding_model = "BAAI/bge-large-en"

    pc = Pinecone(api_key=pinecone_key)
    index_name = "rear-diseas-index"

    if index_name not in [idx["name"] for idx in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(index_name)

    # Optional: index documents if needed (uncomment add_documents once)
    csv_file = "rear_diaease.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        docs = [
            Document(
                page_content=f"PMID: {row['PMID']}\nTitle: {row['Title']}\nAbstract: {row['Abstract']}\nDOI: {row.get('DOI','')}",
                metadata={
                    "row": i,
                    "source": csv_file,
                    "pmid": row["PMID"],
                    "title": row["Title"],
                    "abstract": row["Abstract"],
                    "doi": row.get("DOI", ""),
                },
            )
            for i, row in df.iterrows()
        ]
    else:
        docs = []

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings, text_key="page_content")
    # vectorstore.add_documents(docs)  # run once if you haven't populated the index

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5}, include_metadata=True)

    template = """
    You are a helpful assistant. Answer the user's question based only on the following context.
    If the context does not contain the answer, state that you don't know.

    You are a clinical-science summarization assistant. When asked a question you must:
    - Produce a concise, clear, attractive Markdown answer with: Title, TL;DR, Key Points (bullets), Study Highlights (short table/list), Clinical Implication, and References.
    - Add inline citations using the provided retrieval metadata: show exact PMIDs and link to PubMed when available.
    - Keep total length ~150-350 words. Use bold and short bullets. Use a callout box for the main definition.
    - Output ONLY valid Markdown. Do NOT invent PMIDs

    Context:
    {context}

    Question:
    {question}
    """
    prompt = PromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.3)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa

qa_chain = build_qa_chain()

def format_sources(source_documents):
    lines = []
    for i, doc in enumerate(source_documents, start=1):
        pmid = doc.metadata.get("pmid", "")
        title = doc.metadata.get("title", "")
        doi = doc.metadata.get("doi", "")
        link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""
        parts = [f"{i}. PMID: {pmid}" if pmid else f"{i}. Source"]
        if title:
            parts.append(f"Title: {title}")
        if doi:
            parts.append(f"DOI: {doi}")
        if link:
            parts.append(f"Link: {link}")
        lines.append(" | ".join(parts))
    return "\n".join(lines) if lines else "No sources found."

def answer_question(message, history):
    result = qa_chain.invoke(message)
    answer = result.get("result", "")
    sources = result.get("source_documents", [])
    source_text = format_sources(sources)
    final_md = f"{answer}\n\n---\n\n**Sources**\n\n{source_text}"
    return final_md

qa_css = """
/* Dark style limited to chat history and the input textbox only */
.gradio-container .gr-chatbot {
  background: #0f172a !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
}
.gradio-container .gr-chatbot * {
  color: #e5e7eb !important;
}
.gradio-container .gr-textbox textarea {
  background: #0f172a !important;
  color: #e5e7eb !important;
  border-color: #1f2937 !important;
  caret-color: #93c5fd !important;
}
.gradio-container .gr-textbox textarea::placeholder {
  color: #94a3b8 !important;
}
"""

with gr.Blocks(title="Rare Disease RAG Chat", theme=gr.themes.Soft(neutral_hue="slate", primary_hue="indigo"), css=qa_css) as demo:
    gr.Markdown("## Rare Disease RAG Chat\nAsk clinical questions grounded in your indexed literature.")
    chat = gr.ChatInterface(
        fn=answer_question,
        chatbot=gr.Chatbot(height=400, label="RAG Assistant"),
        textbox=gr.Textbox(placeholder="Ask a question about rare diseases...", container=True, scale=7),
        title="Rare Disease RAG",
        examples=[
            "What are common symptoms of Gaucher disease?",
            "Explain recommended diagnostics for Pompe disease.",
            "Summarize treatment options for Fabry disease."
        ],
        cache_examples=False,
        theme="soft",
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)