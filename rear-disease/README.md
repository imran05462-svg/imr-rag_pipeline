🧬 Rare Disease RAG Chat

An interactive Retrieval-Augmented Generation (RAG) chatbot for rare disease research.
It integrates Pinecone, LangChain, HuggingFace embeddings, and Google Generative AI (Gemini) to provide clinically grounded summaries from indexed literature.

Built with Gradio for a simple, browser-based interface.

🚀 Features

🔍 Context-aware answers retrieved from PubMed-indexed abstracts.

📝 Structured clinical summaries with:

Title, TL;DR, Key Points

Study Highlights (tables/lists)

Clinical Implications

Inline PubMed citations

📚 Custom document indexing from rear_diaease.csv (PMID, Title, Abstract, DOI).

🎨 Dark-mode styled Gradio chat UI.

⚡ Powered by:

Pinecone
 for vector search

LangChain
 for orchestration

BAAI/bge-large-en
 embeddings

Gemini 2.5 Pro
 for LLM responses

📂 Project Structure
├── rear_diaease.csv        # Input dataset (PMID, Title, Abstract, DOI)
├── app.py                  # Main RAG chatbot script
├── requirements.txt        # Dependencies
└── README.md               # Project documentation

🔧 Installation

Clone repo & enter directory:

git clone https://github.com/yourusername/rare-disease-rag.git
cd rare-disease-rag


Create virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Set environment variables in .env:

HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
PINECONE_API_KEY=your_pinecone_key
GOOGLE_API_KEY=your_google_api_key

▶️ Usage

Prepare dataset
Place your rare disease dataset as rear_diaease.csv in the project root.
Expected columns: PMID, Title, Abstract, DOI.

Run the app:

python app.py


Open in browser:
Navigate to http://localhost:7860
.

Ask clinical questions, e.g.:

What are common symptoms of Gaucher disease?

Explain recommended diagnostics for Pompe disease.

Summarize treatment options for Fabry disease.

🛠️ Development Notes

The Pinecone index (rear-diseas-index) is automatically created if it does not exist.

To (re)populate the index with your dataset, uncomment:

vectorstore.add_documents(docs)


All answers include sources with PubMed links.

📌 Example Output
# Gaucher Disease – Clinical Summary

> 🧾 **Definition**: Gaucher disease is a lysosomal storage disorder caused by deficiency of glucocerebrosidase.

**TL;DR:** Gaucher disease presents with hepatosplenomegaly, anemia, and bone involvement. Early enzyme replacement improves outcomes.  

**Key Points:**
- **Cause:** Mutations in GBA1 gene
- **Symptoms:** Splenomegaly, bone crises, anemia
- **Treatment:** Enzyme replacement therapy, substrate reduction therapy

**Study Highlights:**
- [PMID: 123456](https://pubmed.ncbi.nlm.nih.gov/123456/) – ERT improved hematological outcomes  
- [PMID: 789012](https://pubmed.ncbi.nlm.nih.gov/789012/) – SRT effective for mild-moderate cases  

**Clinical Implication:** Early diagnosis and therapy initiation significantly reduce morbidity.  

---
**Sources**
1. PMID: 123456 | Title: Enzyme replacement in Gaucher | DOI: 10.1000/j.jmb.123456 | Link: https://pubmed.ncbi.nlm.nih.gov/123456/

