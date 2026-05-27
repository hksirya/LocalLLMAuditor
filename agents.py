import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import Tool
from langchain_community.chat_models import ChatOllama
from crewai import Agent, Task, Crew, Process

# ==========================================
# CONFIGURATION
# ==========================================
# Pointing to your local Ollama instance
MODEL_NAME = "tinyllama" 
TARGET_PDF = "sample_contract.pdf"

COMPANY_POLICIES = """
1. Payment Terms: Net-60 (60 days) is required. Less than 45 days is a VIOLATION.
2. Jurisdiction: New Delhi courts only. Anything else is a VIOLATION.
"""

print("\n==============================================")
print("  Initializing Air-Gapped AI Swarm (Ollama)   ")
print("==============================================\n")

# ==========================================
# PHASE 1: LANGCHAIN VECTOR MEMORY (RAG)
# ==========================================
def setup_contract_database(pdf_path):
    print("[*] Building Local Vector Database...")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Could not find {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    # Using a free, local HuggingFace embedding model (runs on CPU)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents=pages, embedding=embeddings)
    
    return vectorstore.as_retriever(search_kwargs={"k": 2})

retriever = setup_contract_database(TARGET_PDF)

def search_contract_func(query: str) -> str:
    """Searches the contract database for relevant clauses."""
    # Use the Retriever API to get relevant documents
    try:
        docs = retriever.get_relevant_documents(query)
    except Exception:
        # Fallback for older/newer retriever interfaces
        docs = retriever.get_relevant_documents(query) if hasattr(retriever, "get_relevant_documents") else retriever.get_documents(query)

    return "\n\n".join([doc.page_content for doc in docs])

contract_search_tool = Tool(
    name="Search_Contract",
    description="Use this tool to search the contract. Input a keyword like 'payment' or 'jurisdiction'.",
    func=search_contract_func
)

# ==========================================
# PHASE 2: CREWAI AGENTS (LOCAL OLLAMA)
# ==========================================
print("[*] Booting up TinyLlama Agents...")

# Initialize the local Ollama LLM
local_llm = ChatOllama(model=tinyllama, temperature=0.0)

auditor = Agent(
    role='Compliance Auditor',
    goal='Search the contract and find payment and jurisdiction clauses.',
    backstory='You are a strict auditor. You must use the Search_Contract tool to find information.',
    verbose=True,
    allow_delegation=False,
    tools=[contract_search_tool],
    llm=local_llm
)

reporter = Agent(
    role='Report Writer',
    goal='Format the auditor findings into a clean list.',
    backstory='You write short, clear reports based only on the auditor data.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# ==========================================
# PHASE 3: TASKS
# ==========================================
audit_task = Task(
    description=f"""
    Audit the contract against these policies:
    {COMPANY_POLICIES}
    
    1. Use the Search_Contract tool to search for "payment".
    2. Assess if it violates the Net-60 policy.
    3. Use the Search_Contract tool to search for "jurisdiction".
    4. Assess if it violates the New Delhi policy.
    
    Return a list of the clauses found and your MATCH/VIOLATION assessment.
    """,
    expected_output="A list of found clauses and their assessments.",
    agent=auditor
)

report_task = Task(
    description="""
    Format the Auditor's findings into a clean Markdown table with columns: 
    Clause, Policy, Assessment. Do not add outside information.
    """,
    expected_output="A Markdown table of the findings.",
    agent=reporter
)

# ==========================================
# PHASE 4: EXECUTION
# ==========================================
print("[*] Commencing Swarm Audit...\n")

compliance_crew = Crew(
    agents=[auditor, reporter],
    tasks=[audit_task, report_task],
    process=Process.sequential
)

try:
    final_report = compliance_crew.kickoff()
    print("\n==============================================")
    print("             FINAL AUDIT REPORT               ")
    print("==============================================\n")
    print(final_report)

    with open("Local_Audit_Report.md", "w") as f:
        f.write(str(final_report))
    print("\n[+] Saved report to Local_Audit_Report.md")
    
except Exception as e:
    print(f"\n[!] The swarm encountered a critical error: {e}")
    print("[!] TinyLlama likely failed to parse the tool inputs correctly.")