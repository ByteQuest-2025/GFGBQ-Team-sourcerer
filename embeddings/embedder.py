# # embedder.py

# from utils.azure_integration import generate_embeddings

# class RAGSystem:
#     def __init__(self):
#         self.documents = [
#             "Iron box user manual",
#             "Iron box warranty terms",
#             "Amazon return policy"
#         ]
#         self.embeddings = generate_embeddings(self.documents)

#     def retrieve_document(self, query):
#         query_embedding = generate_embeddings([query])[0]
#         best_match_idx = self._find_best_match(query_embedding)
#         return self.documents[best_match_idx]

#     def _find_best_match(self, query_embedding):
#         cosine_similarities = [
#             self._cosine_similarity(query_embedding, doc_embedding)
#             for doc_embedding in self.embeddings
#         ]
#         return cosine_similarities.index(max(cosine_similarities))

#     def _cosine_similarity(self, vec1, vec2):
#         dot_product = sum(a * b for a, b in zip(vec1, vec2))
#         norm1 = sum(a**2 for a in vec1) ** 0.5
#         norm2 = sum(b**2 for b in vec2) ** 0.5
#         return dot_product / (norm1 * norm2)
