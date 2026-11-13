from agents.state import AgentState
from utils.logger import get_logger

logger = get_logger("WizardOrchestrator")


class WizardOrchestrator:
    """Core routing agent that classifies tasks and directs workflow execution."""

    def __init__(self, name: str = "Wizard-OS-Core"):
        self.name = name

    def route_task(self, state: AgentState) -> AgentState:
        """Analyzes the task description and selects the optimal execution pipeline."""
        logger.info(f"[{self.name}] Evaluating task: '{state.task_description}'")
        task_lower = state.task_description.lower()

        quick_keywords = ("status", "ping", "quick", "health")
        analytics_keywords = ("analytics", "performance", "report", "metrics", "data")

        if any(word in task_lower for word in quick_keywords) and not any(
            word in task_lower for word in analytics_keywords
        ):
            state.route = "QUICK_SUMMARY_PIPELINE"
            state.status = "ROUTED_TO_SYNTHESIZER"
            state.log_step("Orchestrator selected QUICK_SUMMARY_PIPELINE (bypassed heavy analytics).")
            logger.info(f"[{self.name}] Dynamic Route Selected -> {state.route}")
        else:
            state.route = "FULL_ANALYTICS_PIPELINE"
            state.status = "ROUTED_TO_ANALYST"
            state.log_step("Orchestrator selected FULL_ANALYTICS_PIPELINE (full data processing).")
            logger.info(f"[{self.name}] Dynamic Route Selected -> {state.route}")

        return state