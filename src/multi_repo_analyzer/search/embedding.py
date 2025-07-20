from sentence_transformers import SentenceTransformer


def load_embedding_model(model_name="all-MiniLM-L6-v2"):
    print(f"[Embedding] Loading model: {model_name}")
    return SentenceTransformer(model_name)

def embed_chunks(chunks, model):
    results = []
    for chunk in chunks:
        embedding = model.encode(chunk.content)
        results.append({
            "chunk": chunk,
            "embedding": embedding
        })
    return results
