# Air-Gapped AI Compliance Swarm 🛡️

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-Local-orange.svg)](https://ollama.ai/)
[![CrewAI](https://img.shields.io/badge/Framework-CrewAI-red.svg)](https://crewai.com)
[![LangChain](https://img.shields.io/badge/Library-LangChain-green.svg)](https://langchain.com)

An enterprise-grade, **fully local Multi-Agent System (MAS)** designed to automate the auditing of vendor contracts (Master Service Agreements, SLAs, etc.) against strict company policies.

By leveraging **CrewAI**, **LangChain**, and **Ollama**, this system operates 100% offline. No sensitive legal data or proprietary financials are ever sent to public cloud APIs (like OpenAI or Anthropic), ensuring **Zero API Costs** and **Total Data Privacy**.

---

## 🚀 Key Features

*   **100% Air-Gapped:** Runs entirely on your local machine. Ideal for highly sensitive legal and procurement departments.
*   **Semantic RAG Memory:** Uses local vector databases (ChromaDB) to understand the *meaning* of legal text, going beyond brittle keyword matching.
*   **Autonomous Multi-Agent Swarm:** 
    *   **The Compliance Auditor:** Specialized in Fact-Retrieval and policy cross-referencing.
    *   **The Report Writer:** Specialized in executive synthesis and Markdown formatting.
*   **Zero Marginal Cost:** Process 1 or 1,000 contracts for the same price: zero.

---

## 🏗️ System Architecture

1.  **Ingestion:** `PyPDFLoader` ingests and chunks the raw vendor contract.
2.  **Vectorization:** `HuggingFaceEmbeddings` (Local CPU) converts text into mathematical vectors.
3.  **Memory Storage:** Vectors are stored in **ChromaDB**, creating a searchable semantic index.
4.  **Agentic Tooling:** The database is wrapped into a custom LangChain `Tool`, allowing agents to perform autonomous "Semantic Searches."
5.  **Swarm Orchestration:** **CrewAI** manages the sequential "Chain of Thought" as agents collaborate to finalize the audit.

---

## 📋 Prerequisites

### 1. Software Requirements
*   **Python:** 3.9, 3.10, or 3.11 (**Strongly Recommended**).
    *   *Note: Python 3.12+ currently faces compilation issues with several core AI C-libraries.*
*   **Ollama:** Must be installed and running. [Download Ollama here](https://ollama.com/).

### 2. C++ Build Tools (Required)
Because this project compiles C++ libraries (like `greenlet` and `chromadb`) locally, you must have a compiler installed:
*   **Windows:** Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (Select "Desktop development with C++").
*   **Mac:** Run `xcode-select --install`.
*   **Linux:** Run `sudo apt-get install python3-dev build-essential`.

Presentation - [AI Compilance system.pdf](https://github.com/user-attachments/files/28317924/AI.Compilance.system.pdf)
