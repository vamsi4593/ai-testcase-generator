import pandas as pd
from pathlib import Path
from functools import lru_cache
from utils import normalised_test_type

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "updated_rag_testcases.csv"

try:
    @lru_cache(maxsize=None)
    def load_data(path: str) -> pd.DataFrame:
        df = pd.read_csv(path)
        df[["test_case_id", "title", "test_type"]] = df[["test_case_id", "title", "test_type"]].ffill()
        return df
except FileNotFoundError:
    print(f"Error: File is not found at {file_path}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


def document_writer(test_case_type: str):
    if test_case_type is None:
        test_case_type = "both"

    df = load_data(str(file_path))

    df["test_type"] = df["test_type"].str.strip().str.lower()


    mapped_types = normalised_test_type(test_case_type)
    #print(f"mapped types is {mapped_types}")
    mapped_types = [t.strip().lower() for t in mapped_types]

    filtered_df = df[df["test_type"].isin(mapped_types)]

    if filtered_df.empty:
        print(f"No test cases found for type: '{test_case_type}'")
        return []

    result = (
        filtered_df
        .groupby(["test_case_id", "title", "test_type"], sort=False)
        .apply(lambda x: x.to_dict("records"), include_groups=False)
        .to_dict()
    )

    documents = []
    tc_ids = []

    for (tc_id, title, tc_type), rows in result.items():
        tc_scenario = ""
        steps = ""
        expected_result = ""
        summary = ""
        semantic_text = ""
        category = ""

        for row in rows:
            step_num = row.get("step_number", "")

            if not tc_scenario and row.get("scenario"):
                tc_scenario = row["scenario"]

            if row.get("action"):
                steps += f"{step_num}. {row['action']}\n"

            if row.get("expected_result"):
                expected_result += f"{step_num}. {row['expected_result']}\n"

            if not summary and row.get("summary"):
                summary = row["summary"]

            if not semantic_text and row.get("semantic_text"):
                semantic_text = row["semantic_text"]

            if not category and row.get("category"):
                category = row["category"]

        doc_str = (
            f"test case id: {tc_id}\n"
            f"title: {title}\n"
            f"test type: {tc_type}\n"
            f"scenario: {tc_scenario or ''}\n"
            f"steps:\n{steps}"
            f"expected result:\n{expected_result}"
         )

        embed_str = (
            f"title: {title}\n"
            f"steps:\n{steps}\n"
            f"expected result:\n{expected_result}\n"
            f"semantic_text: {semantic_text}\n"
        )

        documents.append(embed_str)
        tc_ids.append(doc_str)

    return {
        "documents": documents,
        "tc_ids": tc_ids
    }

document_writer("functional")