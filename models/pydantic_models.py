from pydantic import BaseModel
from typing import Optional


class Step(BaseModel):
    step_number: Optional[str]
    action: str
    expected_result: str


class TestCase(BaseModel):
    test_case_id: Optional[str]
    title: str
    steps: list[Step]


class TestCases(BaseModel):
    test_cases: list[TestCase]

class Rewrite(BaseModel):
    canonical: str
    expansions : list[str]
