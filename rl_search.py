import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize ChromaDB and embedding model
client = chromadb.Client()
collection = client.get_or_create_collection("content_versions")

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def normalize(vec):
    """
    Normalize vector to unit length (L2 norm = 1)
    """
    norm = np.linalg.norm(vec)
    return vec / norm if norm != 0 else vec

def semantic_search(query_text, top_k=3):
    """
    Perform semantic search for the query using SentenceTransformer and ChromaDB
    """
    if not query_text.strip():
        print("⚠️ Empty query. Please enter a valid search phrase.")
        return {}

    try:
        # Generate and normalize embedding
        embedding = model.encode([query_text])[0]
        embedding = normalize(embedding)

        result = collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=top_k
        )
        return result

    except Exception as e:
        print(f"❌ Error during semantic search: {e}")
        return {}

def display_results(result):
    """
    Display results in a readable format
    """
    if not result or "documents" not in result or not result["documents"][0]:
        print("❌ No matches found.")
        return

    docs = result["documents"][0]
    metas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]  # lower is more similar

    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        distance = distances[i] if i < len(distances) else "?"

        print(f"\n📘 Result {i+1}")
        print(f"📌 Version: {meta.get('version', 'N/A')} | Author: {meta.get('author', 'N/A')} | Tags: {meta.get('tags', 'None')}")
        print(f"🔎 Similarity Score (lower = better): {round(distance, 4)}")
        print(f"📝 Preview:\n{doc[:700]}...\n")
