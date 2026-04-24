# from src.core.parser import ReportParser
# from src.core.processor import ChunkManager

# # 1. Parse
# parser = ReportParser("data/demo_report.txt")
# raw_data = parser.get_raw_text()

# # 2. Chunk
# chunker = ChunkManager()
# processed_chunks = chunker.create_chunks(raw_data)

# print(f"Total Chunks created: {len(processed_chunks)}")
# print(f"First Chunk Preview: {processed_chunks[0][:50]}...")
from src.core.parser import ReportParser
from src.core.processor import ChunkManager
from src.database.vector_store import VectorManager

# 1. Parse & Chunk
parser = ReportParser("data/demo_report.txt")
chunker = ChunkManager()
chunks = chunker.create_chunks(parser.get_raw_text())

# 2. Store in DB
v_db = VectorManager()
v_db.add_chunks(chunks)

# 3. Test Search
search_result = v_db.query_context("How much did we spend on R&D?")
print(f"Bot Memory Result: {search_result}")