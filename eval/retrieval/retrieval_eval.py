import json
from pathlib import Path
from rag import RAGEngine

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "retrieval" / "rag_retrieval_eval_dataset.json"

rag_eng = RAGEngine()

with open(file_path, "r") as eval_dataset:
    eval_dataset_list = json.load(eval_dataset)

count = 0
len_data_set = 0
for eval_dataset in eval_dataset_list:
    for key, value in eval_dataset.items():
        if key == "query":
            tc_id = rag_eng.retrieve_testcases(
                eval_dataset["query"], eval_dataset["test_type"], k=10
            )
            print(f"eval dataset relevant_docs : {eval_dataset['relevant_docs']}")
            count = 0
            Recall = 0
            for i in range(len(tc_id)):
                if tc_id[i] in eval_dataset["relevant_docs"]:
                    len_data_set = len_data_set + len(eval_dataset["relevant_docs"])
                    count += 1
            Recall = count / len(eval_dataset["relevant_docs"])
            print(f"recall@K : {Recall}")
            print(f" hit {count} out of {len(eval_dataset['relevant_docs'])}")
