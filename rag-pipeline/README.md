# 📘 RAG PDF Q&A Application

This project is a **Retrieval-Augmented Generation (RAG)** application built with **LangChain**, **Google Gemini**, and **Pinecone**.  
It allows you to **upload a PDF**, split it into chunks, store embeddings in Pinecone, and query it interactively using Gemini.

---

## 🚀 Features
- Load and split PDF documents into smaller chunks.  
- Generate embeddings using **Google Generative AI**.  
- Store and retrieve document chunks from **Pinecone Vector DB**.  
- Ask questions about the PDF interactively.  

---

## 📂 Project Structure
```
.
├── main.py          # Main RAG application
├── imr-sop.pdf      # Example PDF file (place your own here)
├── .env             # Environment variables
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## 🔧 Prerequisites
Before running the project, ensure you have:

1. **Python 3.9+** installed.  
2. A **Google API Key** for Generative AI (Gemini).  
3. A **Pinecone API Key** and environment.  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-repo/rag-pdf-qa.git
cd rag-pdf-qa
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables  
Create a **.env** file in the project root with the following content:

```env
# Google Generative AI (Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# Pinecone
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
```

⚠️ Replace values with your actual credentials.

### 5️⃣ Add your PDF  
Place the file (e.g., `imr-sop.pdf`) in the project root folder.

---

## ▶️ Run the Application
Run the script:
```bash
python main.py
```

You should see:
```
Environment variables loaded successfully.
Loading and splitting the document...
Document split into 25 chunks.
Initializing models and Pinecone...
Pinecone vector store is ready.
RAG chain created.

RAG Q&A Ready! Type your question (or 'exit' to quit)
```

Now you can start asking questions about your PDF.

---

## 📝 Example Usage
```
Enter your question: What is the purpose of this document?

================================================================================
Q: What is the purpose of this document?
--------------------------------------------------------------------------------
A: The purpose of this document is to outline...
================================================================================
```

---

## 📦 Requirements File (`requirements.txt`)
```txt
python-dotenv
langchain
langchain-community
langchain-google-genai
langchain-pinecone
pinecone-client
```

---

## ✅ Notes
- Ensure the PDF file is not too large; otherwise, consider reducing the chunk size.  
- If the Pinecone index already exists, the script will connect automatically.  
- To exit, type `exit` or `quit` in the Q&A loop.  
