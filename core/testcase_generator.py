import config
from openai import OpenAI
from models import pydantic_models as Pm
from rag import RAGEngine


class TestCaseGenerator:
    def __init__(self):
        self.rag = RAGEngine()

    def prompt_builder(self, requirement, test_type):
        test_case_type = self.normalised_test_type(test_type)
        initial_prompt = f"Generating {test_case_type} test cases for {requirement}"
        print(f"------ user prompt: {initial_prompt}")
        context_prompt = self.rag.create_context_prompt(initial_prompt, test_case_type, k=6)
        prompt = f"""
        I am providing reference test cases from our database to show you the expected format and level of detail.

        ### REFERENCE SAMPLES (Do not copy these):
        {context_prompt}


        ### YOUR TASK:
        Generate BRAND NEW, unique {test_case_type}(positive, negative and edge) test cases for this requirement: "{requirement}"
        The output must follow the style of the references but contain different steps and logic specific to the new requirement.
        """
        return prompt

    def normalised_test_type(self,test_case_type):
        test_type_map = {
            "functional": "Functional",
            "non-functional": "Non-Functional",
            "both": "Functional and Non-Functional",
        }
        return test_type_map[test_case_type]

    def generate_testcase(self, requirement, test_type):
        prompt_text = self.prompt_builder(requirement, test_type)
        client = OpenAI()
        responses = client.responses.parse(
            model=config.MODEL_NAME, input=prompt_text, text_format=Pm.TestCases
        )

        testcases = responses.output_parsed

        for i, testcase in enumerate(testcases.test_cases, 1):
            testcase.test_case_id = f"TC{i:03}"
            for j, step in enumerate(testcase.steps, 1):
                step.step_number = f"{j}"
        return testcases.test_cases