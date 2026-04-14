import config
from openai import OpenAI
from models import pydantic_models as Pm
from .validations import Validate


class Rewriter:

    def __init__(self):
        self.client = OpenAI()
        self.validate = Validate()

    def rewrite_prompt(self, prompt, retry =0):
        prompt_rewrite_text = f"""Rewrite the following query into QA-style phrases for retrieval:
        {prompt}

        Rules:
        * Preserve exact intent
        * Do not introduce new scenarios
        * Keep condition and outcome unchanged
        * Do not generate test cases
        * Do not include steps or expected results
        * Do not explain anything
        * Only rewrite the query with semantic variations within the same intent

        Language style:
        * Use formal QA/test-case language
        * Use only validation verbs: Verify, Validate, Ensure
        * Avoid conversational phrasing like "does not go through", "doesn't work"
        * Keep sentences concise and avoid unnecessary elaboration

        Intent constraints:
        * Do not change the direction of intent
        * If query describes failure, rewrite as failure
        * If query describes success, rewrite as success
        * Do not replace key entities or conditions with unrelated terms

        Variation requirements:
        * Each expansion must vary wording while preserving intent
        * Introduce domain-specific vocabulary variations for key terms
        * Replace important words with equivalent concepts used in real systems
        * Avoid repeating identical sentence structures
        * Avoid reusing the same key nouns across all expansions
        * Ensure at least one expansion uses significantly different terminology from the original query

        Examples:
        * "invalid input" → "malformed data", "incorrect value", "unexpected input"
        * "login failure" → "authentication error", "access denied", "login rejection"
        * "payment failure" → "transaction decline", "payment rejection", "authorization failure"
        * "SQL injection" → "malicious input", "injection attack", "unsanitized input"

        Output format:
        Return ONLY a JSON object:
        {{
        "canonical": "string",
        "expansions": ["string", "string", "string"]
        }}

        Constraints:
        * Generate exactly 3 expansions
        * Canonical must be the closest direct QA-style rewrite of the original query
        * Canonical must start with Verify / Validate / Ensure
        * Each expansion must start with Verify / Validate / Ensure
        * Do not include any extra text outside the JSON
        * Do not introduce new actors (e.g., attacker, user) unless explicitly present in the original query
        """

        response = self.client.responses.parse(
            model=config.MODEL_NAME, input=prompt_rewrite_text, text_format=Pm.Rewrite
        )
        print(f"\n response is {response.output_parsed} \n")

        return response.output_parsed