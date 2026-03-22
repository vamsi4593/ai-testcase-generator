import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "payment_testcases_formatted.csv"


def document_writer(test_case_type):

    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_colwidth", None)

    df = pd.read_csv(file_path).ffill()

    result = (
        df.groupby(["test_case_id", "title", "test_type"])
        .apply(lambda x: x.to_dict("records"), include_groups=False)
        .to_dict()
    )

    # result = {f'{test_case_id} - {title}': rows for (test_case_id, title), rows in result.items()}

    documents = []
    for key in result.keys():
        doc_str = f"test case id : {key[0]}\ntitle : {key[1]}\ntest type : {key[2]}\n"
        expected_result = ""
        for row in result[key]:
            for row_key in row:
                if row_key == "step_number" or row_key == "action":
                    continue
                expected_result = f"{row[row_key]}"
        doc_str += f"expected result : {expected_result}\n"
        documents.append(doc_str)
    filtered_doc = [doc for doc in documents if test_case_type in doc]
    return filtered_doc


document_writer("functional")
