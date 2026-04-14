from core import TestCaseGenerator
from utils import export_csv as Exp

tg = TestCaseGenerator()

print("---------- AI Test Case Generator ----------")
requirement = input("Please enter your requirement: ")

valid_types = ["functional", "non-functional", "both"]
test_type = input("Please enter your test type: ").strip().lower()

while test_type not in valid_types:
    print("Invalid type. Please enter: functional, non-functional, or both.")
    test_type = input("Please enter your test type: ").strip().lower()

def display_test_cases(test_cases):
    for testcase in test_cases:
        print("-" * 60)
        print(f"{testcase.test_case_id}    -   {testcase.title}")
        print("-" * 60)
        for step in testcase.steps:
            print(f"{step.step_number}. {step.action}")
            print(f"   Expected Result: {step.expected_result} \n")


testcases = tg.generate_testcase(requirement, test_type)
display_test_cases(testcases)

export_test_cases = input(
    "Do you want to export the test cases to CSV file ? y/n : "
).lower()
while export_test_cases not in ["y", "n"]:
    print("Please enter y/n")
    export_test_cases = input("Please enter y/n: ")

if export_test_cases == "y":

    default_name = Exp.default_file_name(requirement)
    csv_file_name = input(
        f"Please enter your csv file name(default name: {default_name}) : "
    )
    if csv_file_name == "":
        csv_file_name = default_name
    csv_content = Exp.build_csv_data(testcases)
    Exp.write_csv(csv_content, csv_file_name)

    print(f"testcase exported to {csv_file_name}")
