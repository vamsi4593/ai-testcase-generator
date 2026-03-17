import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rag import documents as doc

model = SentenceTransformer('all-MiniLM-L6-v2')
test_case_type = "Functional"
document = doc.document_writer(test_case_type)

doc_embeddings = model.encode(document).astype(np.float32)

n, d = doc_embeddings.shape
print(n, d)

dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
faiss.write_index(index, "testcases.index")
index.add(doc_embeddings)


def create_context_prompt(input_prompt, k):

    embedded_in_prompt = model.encode([input_prompt]).astype(np.float32)

    distances, indices = index.search(embedded_in_prompt, k)

    print(f"distance is : {distances}")
    print(f"matching indices is :{indices}")
    print("----------Retrieved documents are : ----------")
    context_prompt = ""
    for i in indices.flatten():
        if test_case_type in document[i]:
            print( {document[i]})
        context_prompt += document[i]
    return context_prompt
