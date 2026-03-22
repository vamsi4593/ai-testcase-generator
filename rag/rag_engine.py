import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rag import documents as doc
import os

class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.threshold = 0.45


    # TODO: Add detailed comments explaining RAG flow and retrieval decisions

    def get_document(self,test_case_type):
        document = doc.document_writer(test_case_type)

        return document

    def get_doc_embeddings(self,test_case_type):
        model = self.model
        document = self.get_document(test_case_type)
        doc_embeddings = model.encode(document).astype(np.float32)

        return doc_embeddings

    def load_index(self, test_case_type):
        if os.path.exists(f"testcases_{test_case_type}.index"):
            index = faiss.read_index(f"testcases_{test_case_type}.index")
            return index
        else:
            return None

    def build_index(self, test_case_type):
        doc_embeddings = self.get_doc_embeddings(test_case_type)
        dimension = doc_embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(doc_embeddings)
        faiss.write_index(index, f"testcases_{test_case_type}.index")

        return index


    def create_context_prompt(self, input_prompt, test_case_type, k):
        model = self.model
        document = self.get_document(test_case_type)
        embedded_in_prompt = model.encode([input_prompt]).astype(np.float32)
        index = self.load_index(test_case_type)
        if index is None:
            index = self.build_index(test_case_type)
        distances, indices = index.search(embedded_in_prompt, k)
        threshold = self.threshold
        mask = distances[0] >= threshold
        filtered_indices = indices[0][mask]
        filtered_distances = distances[0][mask]

        print(f"distance before threshold is : {distances} and after is : {filtered_distances}")
        print(f"matching indices before threshold is {indices} and after is :{filtered_indices}")
        print("----------Retrieved documents after similarity filtering: ----------")
        for i in filtered_indices.flatten():
            print(f"{i} : {document[i]}\n")
        context_prompt: str = ""

        for i in filtered_indices.flatten():
            context_prompt += f"\n{document[i]}"

        return context_prompt