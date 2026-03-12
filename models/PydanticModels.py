from pydantic import BaseModel
from typing import Optional

class TestCases(BaseModel):
    test_cases: list[TestCase]


class TestCase(BaseModel):
    test_case_id: Optional[str]
    title: str
    Steps: list[Step]


class Step(BaseModel):
    step_number: Optional[str]
    action: str
    expected_result: str
