from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from groq import Groq
from dotenv import load_dotenv

import tempfile
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
class ConversationMemory:

    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

    def add_ai_message(self, message):
        self.history.append({
            "role": "assistant",
            "content": message
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []
def load_pdf(uploaded_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_path = temp_file.name

    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    os.remove(temp_path)

    return documents


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = text_splitter.split_documents(documents)

    return chunks
def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_store
def retrieve_chunks(vector_store, question, k=4):
    """
    Retrieve the most relevant chunks for the user's question.
    """

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results
def build_prompt(question, documents, history):

    history_text = ""

    for msg in history:
        history_text += f"{msg['role'].capitalize()}: {msg['content']}\n"

    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    prompt = f"""
You are a helpful AI assistant.

Use the conversation history and the retrieved context to answer the user's question.

If the answer is not available in the context, reply:
"I couldn't find the answer in the uploaded PDF."

Conversation History:
{history_text}

Context:
{context}

Current Question:
{question}

Answer:
"""

    return prompt
def generate_answer(question, documents, history):

    prompt = build_prompt(
        question,
        documents,
        history
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content