import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime

client = chromadb.Client()
collection = client.get_or_create_collection("content_versions")
model = SentenceTransformer("all-MiniLM-L6-v2")

def add_version(doc_text, doc_id, version_num=None, author="Unknown", tags=None):
    existing = collection.get(where={"doc_id": doc_id})
    existing_versions = [meta.get('version', 0) for meta in existing.get("metadatas", [])]
    version_num = version_num or (max(existing_versions, default=0) + 1)

    metadata = {
    "doc_id": doc_id,
    "version": version_num,
    "author": author,
    "tags": ", ".join(tags) if tags else "",
    "timestamp": datetime.now().isoformat()
}


    embedding = model.encode(doc_text).tolist()

    collection.add(
        documents=[doc_text],
        metadatas=[metadata],
        ids=[f"{doc_id}_v{version_num}"],
        embeddings=[embedding]
    )
    print(f"[+] Version {version_num} saved for '{doc_id}'")

def query_content(text_query, top_k=3):
    embedding = model.encode([text_query])[0]
    return collection.query(query_embeddings=[embedding.tolist()], n_results=top_k)

def get_by_version(doc_id, version_num):
    return collection.get(ids=[f"{doc_id}_v{version_num}"])

def get_next_version_num(doc_id="chapter1"):
    results = collection.get(where={"doc_id": doc_id})
    versions = [int(m['version']) for m in results.get("metadatas", []) if m.get("version") is not None]
    return max(versions, default=0) + 1
