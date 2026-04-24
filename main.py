import json
from src.core.parser import ReportParser
from src.core.processor import ChunkManager
from src.database.vector_store import VectorManager
from src.api.client import LLMClient

def run_quiz_pipeline(file_path):
    print(f"--- Starting Pipeline for {file_path} ---")
    
    # 1. Parsing & Chunking
    parser = ReportParser(file_path)
    chunker = ChunkManager()
    raw_text = parser.get_raw_text()
    chunks = chunker.create_chunks(raw_text)
    
    # 2. Vector Indexing
    v_db = VectorManager()
    v_db.add_chunks(chunks)
    
    # 3. Retrieval
    # We ask the DB for facts specifically related to "performance" and "metrics"
    context = v_db.query_context("financial performance and strategic milestones", n_results=8)
    
    # 4. LLM Generation
    llm = LLMClient()
    raw_response = llm.generate_quiz_data(context)
    
    # 5. Result
    print("\n--- Pipeline Complete ---")
    return raw_response

if __name__ == "__main__":
    quiz = run_quiz_pipeline("data/demo_report.txt")
    print(quiz)