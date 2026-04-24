from src.database.vector_store import VectorManager

def load_report():
    db = VectorManager()
    
    # Read your specific report
    with open("data/demo_report.txt", "r") as f:
        content = f.read()
    
    # Simple chunking by paragraph (or use a better splitter)
    chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 10]
    
    db.add_chunks(chunks)
    print(f"✅ Successfully indexed {len(chunks)} chunks into chroma_db/")

if __name__ == "__main__":
    load_report()