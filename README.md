# 🚀 AI-Based Finance Quiz System


## 📌 Project Overview
The **AI-Based Finance Quiz System** is a RAG-powered (Retrieval-Augmented Generation) application designed to enhance financial literacy. It allows users to select complex financial reports, generates dynamic quizzes using Llama 3.3, and provides a personalized study guide based on user performance.

### Key Features:
* **Dynamic RAG Pipeline:** Uses ChromaDB and Groq (Llama 3.3) to generate factually grounded questions.
* **Document Selector:** Switch between multiple financial reports (Annual Reports, ESG, Risk Disclosures).
* **Smart Shuffling:** Questions and options are randomized for every session.
* **Study Report Export:** Generates a professional PDF study guide highlighting explanations for the user.
* **High Performance:** Optimized for low-latency using Groq's LPU inference.

---

## 🏗️ Architecture
The system follows a 3-tier architecture:
1.  **Frontend:** Streamlit for a highly interactive user experience.
2.  **Backend:** Python logic handling the RAG workflow and API orchestration.
3.  **Data Layer:** ChromaDB as a local vector store for high-speed semantic retrieval.

---

## 🛠️ Tech Stack
* **LLM Engine:** Llama 3.3 (via Groq Cloud API)
* **Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **Web Framework:** Streamlit
* **Language:** Python 3.9+
* **Documentation Export:** FPDF

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed. You will also need a **Groq API Key**.

### 2. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
