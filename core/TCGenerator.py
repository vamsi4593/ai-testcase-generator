import config
from openai import OpenAI
import models.PydanticModels as Pm


def prompt_builder(requirement, test_type):
    test_case_type = normalised_test_type(test_type)
    return f"Generating {test_case_type} test cases for {requirement}"

def normalised_test_type(test_case_type):
    test_type_map = {
        "functional": "functional",
        "non-functional": "non-functional",
        "both": "functional and non-functional"
    }
    return test_type_map[test_case_type]

def generate_testcase(requirement, test_type):
    prompt_text = prompt_builder(requirement, test_type)
    client = OpenAI()
    responses =  client.responses.parse(
        model = config.MODEL_NAME,
        input= prompt_text,
        text_format = Pm.TestCases
        )

    testcases = responses.output_parsed

    for i, testcase in enumerate(testcases.test_cases, 1):
        testcase.test_case_id = f"TC{i:03}"
        for j,step in enumerate(testcase.Steps, 1):
            step.step_number = f"{j}"
    return testcases.test_cases
