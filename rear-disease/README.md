# 🧬 Rare Disease RAG Chat

A **Retrieval-Augmented Generation (RAG)** pipeline for answering clinical questions about **rare diseases**, using **LangChain**, **Pinecone**, **HuggingFace embeddings**, and **Google Gemini models**.  
The app is deployed with a **Gradio UI** for interactive Q&A.

---

## 🚀 Features
- Index biomedical literature (CSV with PMID, Title, Abstract, DOI).
- Store embeddings in **Pinecone** for fast retrieval.
- Query pipeline built with **LangChain RetrievalQA**.
- Uses **HuggingFace embeddings (`BAAI/bge-large-en`)**.
- Answers are generated using **Google Gemini (gemini-2.5-pro)**.
- Responses are returned in **structured Markdown**:
  - Title
  - TL;DR
  - Key Points
  - Study Highlights
  - Clinical Implication
  - References (with PubMed links)

---

## 📦 Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/yourusername/rare-disease-rag.git
cd rare-disease-rag

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```ini
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_genai_api_key
```

---

## 📂 Data Preparation

Place your dataset in the root folder as `rear_diaease.csv` with the following columns:

- `PMID`
- `Title`
- `Abstract`
- `DOI` (optional)

Example:

| PMID     | Title                        | Abstract                 | DOI         |
|----------|------------------------------|--------------------------|-------------|
| 12345678 | Study on Gaucher disease     | Gaucher disease is...    | 10.1000/j.j |

---

## ▶️ Run the App

```bash
python app.py
```

The Gradio app will be available at:

```
http://0.0.0.0:7860
```

---

## 💻 Usage

- Open the Gradio UI.
- Type a question like:
  - *"What are common symptoms of Gaucher disease?"*
  - *"Explain recommended diagnostics for Pompe disease."*
  - *"Summarize treatment options for Fabry disease."*
- Get a **structured Markdown response** with inline PubMed references.

---

## 🛠️ Tech Stack

- **LangChain** – RAG pipeline
- **Pinecone** – Vector DB
- **HuggingFace** – Embeddings
- **Google Gemini** – LLM
- **Gradio** – UI
- **Pandas** – Data handling
- **dotenv** – Secrets management

---

## 📌 Example Output

```markdown
### Gaucher Disease – Clinical Summary

> ⚕️ **Definition:** Gaucher disease is an autosomal recessive lysosomal storage disorder caused by mutations in the GBA gene.

**TL;DR:** Gaucher disease manifests with hepatosplenomegaly, bone crises, cytopenias, and may require enzyme replacement therapy.

**Key Points**
- **Genetic Basis:** GBA mutations
- **Symptoms:** Hepatosplenomegaly, anemia, thrombocytopenia, bone pain
- **Diagnosis:** Enzyme assay, genetic testing
- **Treatment:** Enzyme replacement therapy, substrate reduction therapy

**Study Highlights**
- Prevalence higher in Ashkenazi Jewish population
- Early diagnosis improves outcomes
- Novel therapies under clinical evaluation

**Clinical Implication**
- Early recognition reduces disease burden.
- Genetic counseling recommended.

**References**
1. PMID: 12345678 | Title: Study on Gaucher disease | DOI: 10.1000/j.j | [Link](https://pubmed.ncbi.nlm.nih.gov/12345678/)
```

---

## 📜 License
MIT License – feel free to use and modify.

---

## 🤝 Contributing
Pull requests are welcome. Please open an issue first to discuss proposed changes.
