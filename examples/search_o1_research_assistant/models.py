from typing import List
from dataclasses import dataclass, field

@dataclass
class ResearchTopic:
    main_query: str
    sub_queries: List[str] = field(default_factory=list)

@dataclass
class ResearchReport:
    topic: ResearchTopic
    summary: str = ""
    key_insights: List[str] = field(default_factory=list)