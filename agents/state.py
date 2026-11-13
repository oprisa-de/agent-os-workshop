from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class AgentState:
    """Shared state object passed across nodes in the multi-agent workflow."""
    task_description: str
    route: str = "UNASSIGNED"
    status: str = "INITIALIZED"
    metrics: Dict[str, Any] = field(default_factory=dict)
    ai_insights: str = ""
    final_report: str = ""
    execution_history: List[str] = field(default_factory=list)

    def log_step(self, step_note: str) -> None:
        """Appends an execution trace entry to the state history."""
        self.execution_history.append(step_note)