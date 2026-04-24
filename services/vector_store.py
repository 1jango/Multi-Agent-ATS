import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        # Using a lightweight model for embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension for MiniLM
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []

    def add_candidate(self, cv_text: str, candidate_name: str):
        """Encodes CV text and adds it to the FAISS index."""
        embedding = self.model.encode([cv_text])
        self.index.add(np.array(embedding).astype('float32'))
        self.metadata.append(candidate_name)

    def search_similar(self, query_text: str, top_k: int = 3):
        """Finds the most similar past candidates for a given JD or skill."""
        query_embedding = self.model.encode([query_text])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        return [self.metadata[i] for i in indices[0] if i != -1]