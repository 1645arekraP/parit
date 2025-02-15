from dataclasses import dataclass
from typing import List, Optional

@dataclass
class QuestionResponse():
    ac_rate: float
    content: str
    difficulty: str
    example_test_cases: str
    hints: str
    is_paid: bool
    link: str
    title: str
    title_slug: str
    topic_tags: List[str]

@dataclass
class SolutionResponse():
    title: str
    title_slug: str
    timestamp: str
    lang: str
    runtime: str
    memory: str
    time: str
    status: str

@dataclass
class DailyQuestionResponse():
    pass

@dataclass
class SolutionResponseList():
    total: int
    solutions: List[SolutionResponse]

@dataclass
class QuestionListResponseList():
    total: int
    questions : List[QuestionResponse]

@dataclass
class ProfileResponse():
    pass