import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rag import documents as doc
from .rewriter import Rewriter
import os


class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = 0.0
        self.rewrite = Rewriter()

    # TODO: Add detailed comments explaining RAG flow and retrieval decisions

    def get_document(self, test_case_type):

        data = doc.document_writer(test_case_type)

        return data

    def get_doc_embeddings(self, test_case_type):
        model = self.model
        document = self.get_document(test_case_type)["documents"]
        doc_embeddings = model.encode(document).astype(np.float32)
        faiss.normalize_L2(doc_embeddings)
        print("Doc norm sample:", np.linalg.norm(doc_embeddings[0]))

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

    def retrieved_indices(self, embedded_in_prompt, test_case_type, k):
        k_value = k
        index = self.load_index(test_case_type)
        if index is None:
            index = self.build_index(test_case_type)
        distances, indices = index.search(embedded_in_prompt, k_value)
        print(f"distances : {distances}")
        threshold = self.threshold
        mask = distances[0] >= threshold
        filtered_indices = indices[0][mask]
        return filtered_indices

    def create_context_prompt(self, input_prompt, test_case_type, k):
        model = self.model
        document = self.get_document(test_case_type)["documents"]
        query_rewrite = self.rewrite.rewrite_prompt(input_prompt)
        print(f"query_rewrite: {query_rewrite}")
        query_list = [input_prompt] + [query_rewrite.canonical] + query_rewrite.expansions
        print(f"query_list: {query_list}")
        doc_dict = {}
        for query in query_list:
            embedded_query = model.encode([query]).astype(np.float32)
            faiss.normalize_L2(embedded_query)
            indices = self.retrieved_indices(embedded_query, test_case_type, k)
            print(f"indices are {indices}")
            for i in indices.flatten():
                if document[i] in doc_dict:
                    doc_dict[document[i]] += 1
                else:
                    doc_dict[document[i]] = 1
        context_docs = []
        print(doc_dict)
        for doc in doc_dict:
            if doc_dict[doc] >=1:
                context_docs.append(doc)

        context_prompt = " ".join(context_docs)
        print(f"context_prompt : {context_prompt}")

        return context_prompt

    def retrieve_testcases(self, query, test_case_type=None, k=1):
        model = self.model
        test_cases = self.get_document(test_case_type)["tc_ids"]
        query_rewrite = self.rewrite.rewrite_prompt(query)
        print(f"query_rewrite: {query_rewrite}")
        query_list = [query] + [query_rewrite.canonical] + query_rewrite.expansions
        print(f"query_list: {query_list}")
        tc_id = {}

        for query in query_list:
            embedded_query = model.encode([query]).astype(np.float32)
            faiss.normalize_L2(embedded_query)
            indices = self.retrieved_indices(embedded_query, test_case_type, k)
            print(f"indices are {indices}")
            for i in indices.flatten():
                if test_cases[i] in tc_id:
                    tc_id[test_cases[i]] += 1
                else:
                    tc_id[test_cases[i]] = 1

        tc_ids = []
        for tc in tc_id:
            if tc_id[tc]>=1:
                tc_ids.append(tc.split('\n')[0].split(':')[1].strip(' '))
        print(f"tc_ids : {tc_ids}")
        return tc_ids

