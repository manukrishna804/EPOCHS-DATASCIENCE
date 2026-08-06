# 📄 PDF Question Answering Application using RAG

## Participant Details
- Name: Manu Krishna C.K.
- MUID: manukrishnack-1@mulearn

A Streamlit-based Retrieval-Augmented Generation (RAG) application that allows users to upload a PDF and ask questions in natural language. The application retrieves the most relevant content from the uploaded document using semantic search and generates context-aware answers using the Groq LLM API.

---

# 🚀 Features

* 📄 Upload any PDF document
* ✂️ Automatic document chunking
* 🧠 Semantic search using vector embeddings
* 📚 FAISS in-memory vector database
* 🤖 AI-powered question answering using Groq
* 💬 Conversation memory for follow-up questions
* 📑 Source citations for every response
* ⚡ Simple and interactive Streamlit interface

---

# 🏗️ Project Architecture

```
                Upload PDF
                     │
                     ▼
              PyPDFLoader
                     │
                     ▼
      RecursiveCharacterTextSplitter
                     │
                     ▼
      Sentence Transformer Embeddings
                     │
                     ▼
                 FAISS Vector Store
                     │
                     ▼
              Similarity Search
                     │
                     ▼
          Top Relevant Chunks
                     │
                     ▼
        Conversation History
                     │
                     ▼
                 Groq LLM
                     │
                     ▼
               Generated Answer
```

---

# 🛠️ Technologies Used

| Component             | Technology                             |
| --------------------- | -------------------------------------- |
| UI                    | Streamlit                              |
| PDF Loader            | PyPDFLoader (LangChain Community)      |
| Text Splitter         | RecursiveCharacterTextSplitter         |
| Embedding Model       | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database       | FAISS                                  |
| LLM                   | Groq API (Llama 3.3 70B Versatile)     |
| Conversation Memory   | Custom ConversationMemory Class        |
| Environment Variables | python-dotenv                          |

---

# 📂 Project Structure

```
pdf-qa-rag-assistant/

│
├── app.py
├── rag_pipeline.py
├── requirements.txt
├── README.md
├── .env
├── chroma_db/
├── sample_data/
└── screenshots/
```

---

# 🔄 RAG Pipeline

### 1. Load PDF

The uploaded PDF is read using **PyPDFLoader** from LangChain Community.

---

### 2. Split into Chunks

The document is divided into smaller overlapping chunks using:

* Chunk Size: **1000**
* Chunk Overlap: **150**

This preserves context while improving retrieval quality.

---

### 3. Generate Embeddings

Each chunk is converted into a vector using:

```
sentence-transformers/all-MiniLM-L6-v2
```

These embeddings capture the semantic meaning of the text.

---

### 4. Store in FAISS

The embeddings are stored inside an in-memory FAISS vector database.

The vector database is created once per uploaded document and reused during the session.

---

### 5. Retrieve Relevant Chunks

For every user question:

* the question is embedded,
* FAISS performs similarity search,
* the top **4** most relevant chunks are retrieved.

---

### 6. Generate Answer

The retrieved chunks together with the conversation history are sent to the Groq LLM.

The model generates an answer strictly based on the retrieved document context.

---

# 💬 Conversation Memory

A lightweight custom `ConversationMemory` class maintains chat history.

Each interaction is stored as:

* User Message
* Assistant Response

The stored history is included in every new prompt sent to Groq, allowing the assistant to understand follow-up questions such as:

* "Explain XGBoost."
* "What are its advantages?"
* "Where is it used?"

---

# 📄 Source Citations

Every answer includes the retrieved document chunks used to generate the response.

Each source displays:

* Source Number
* PDF Page Number
* Retrieved Chunk Text

This improves transparency and allows users to verify the generated answer.

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/pdf-qa-rag-assistant.git

cd pdf-qa-rag-assistant
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=your_groq_api_key
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---



# ☁️ Deployment on Streamlit Community Cloud

This project is optimized for deployment on Streamlit Community Cloud. 

1. Fork or upload this repository to your GitHub account.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in.
3. Click **New app** and authorize GitHub if needed.
4. Select the repository, branch, and set the main file path as `app.py`.
5. Click **Advanced settings...** and add your Groq API key in the **Secrets** field:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```
6. Click **Save** and then **Deploy!**

> **Note:** FAISS is used instead of ChromaDB because it works entirely in-memory and avoids common SQLite3 version conflicts on Streamlit Cloud, ensuring stable and reliable deployment.

---

# ⚠️ Challenges Faced

* Integrating LangChain with the latest package structure.
* Managing conversation history across Streamlit reruns.
* Preventing repeated creation of the vector database.
* Designing prompts that use only retrieved document context.
* Displaying retrieved source chunks alongside generated answers.

---

# 🚀 Future Improvements

* Support multiple PDFs simultaneously.
* Streaming responses.
* Highlight relevant text directly inside the PDF.
* Add model selection from the UI.
* Display similarity scores for retrieved chunks.
* Deploy with Docker.

---

# 👨‍💻 Author

**Manu Krishna**

B.Tech Information Technology

Government Engineering College Palakkad

---

# 📄 License

This project is developed for educational purposes as part of the **Epochs '26 Assignment 11**.
