from typing import List, TypedDict, Optional

class DebateState(TypedDict):
    topic: str
    messages: List[dict]  # [{"round": 1, "agent": "Scientist", "content": "..."}]
    current_round: int
    current_agent: str    # "Scientist" or "Philosopher"
    winner: Optional[str]
    reason: Optional[str]
    is_mock: bool
