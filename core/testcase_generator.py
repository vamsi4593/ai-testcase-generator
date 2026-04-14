import config
from openai import OpenAI
from models import pydantic_models as Pm
from rag import RAGEngine


class TestCaseGenerator:
    def __init__(self):
        self.rag = RAGEngine()
        self.client = OpenAI()

    def prompt_builder(self, requirement, test_type):
        initial_prompt = f"Generating {test_type} test cases for {requirement}"
        print(f"------ user prompt: {initial_prompt}----------")
        context_prompt = self.rag.create_context_prompt(
            requirement, test_type, k=3
        )
        prompt = f"""
        I am providing reference test cases from our database to show you the expected format and level of detail.

        ### REFERENCE SAMPLES (Do not copy these):
        {context_prompt}


        ### YOUR TASK:
        Generate BRAND NEW, unique {test_type}(positive, negative and edge) test cases for this requirement: "{requirement}"
        The output must follow the style of the references but contain different steps and logic specific to the new requirement.
        """
        print(f"------ final user prompt: {prompt}")
        return prompt

    def generate_testcase(self, requirement, test_type):
        prompt_text = self.prompt_builder(requirement, test_type)
        responses = self.client.responses.parse(
            model=config.MODEL_NAME, input=prompt_text, text_format=Pm.TestCases
        )
        print(f"\n response is {responses.usage} \n")

        testcases = responses.output_parsed

        for i, testcase in enumerate(testcases.test_cases, 1):
            testcase.test_case_id = f"TC{i:03}"
            for j, step in enumerate(testcase.steps, 1):
                step.step_number = f"{j}"
        return testcases.test_cases

    def rewrite_prompt(self, prompt):
        prompt_rewrite_text = f"""
        You rewrite {prompt} into QA-style phrases for retrieval
        
        First, identify:
        - action
        - entity
        - condition

        Then rewrite based on these elements.

        Rules:
        - Preserve exact intent
        - Do not introduce new scenarios
        - Keep condition and outcome unchanged
        - Do not generate test cases
        - Do not include steps or expected results
        - Do not explain anything
        - Only rewrite the query with semantic variations within same intent
        - Do not use phrases like:
            - generating test cases
            - creating scenarios
            - formulating cases

        Use only validation language:
        - Verify
        - Validate
        - Ensure
        
        Ensure diversity in expansions:
        - Include both functional validation phrasing and failure-oriented phrasing (if applicable)
        - Each expansion should vary wording or structure meaningfully
        
        Return ONLY a JSON object with fields:
        - canonical
        - expansion
        Generate exactly 3 expansions
        Do not include any extra text.
        """
        response = self.client.responses.parse(
            model=config.MODEL_NAME, input=prompt_rewrite_text, text_format=Pm.Rewrite
        )
        print(f"\n response is {response.output_parsed} \n")



