import csv
import io


def default_file_name(requirement):
    return f"{requirement.replace(' ','_')}.csv"


def _testcases_to_rows(test_cases):

    rows = []
    for test_case in test_cases:
        for step in test_case.steps:

            if step.step_number == "1":
                rows.append(
                    {
                        "test_case_id": test_case.test_case_id,
                        "title": test_case.title,
                        "step_number": step.step_number,
                        "action": step.action,
                        "expected_result": step.expected_result,
                    }
                )
            else:
                rows.append(
                    {
                        "test_case_id": "",
                        "title": "",
                        "step_number": step.step_number,
                        "action": step.action,
                        "expected_result": step.expected_result,
                    }
                )

    return rows


def build_csv_data(test_cases):

    rows = _testcases_to_rows(test_cases)

    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "test_case_id",
            "title",
            "step_number",
            "action",
            "expected_result",
        ],
    )

    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()


def write_csv(csv_content, file_name):

    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        csvfile.write(csv_content)
