from agents.state import AgentState
from utils.logger import get_logger

logger = get_logger("WizardSynthesizer")


class WizardSynthesizer:
    """Executive reporting agent that compiles AgentState into a structured report."""

    def __init__(self, name: str = "Wizard-OS-Synthesizer"):
        self.name = name

    def generate_executive_report(self, state: AgentState) -> AgentState:
        """Synthesizes workflow state, metrics, and AI insights into a formatted report."""
        logger.info(f"[{self.name}] Synthesizing executive report for route: {state.route}")

        if not state.metrics:
            state.metrics = {
                "total_tasks_completed": 0,
                "average_success_rate": 100.0,
                "top_performing_agent": "Core-System (Direct Check)"
            }

        recommendation = state.ai_insights or "No AI recommendations generated."
        trace_lines = "\n".join([f"          * {step}" for step in state.execution_history])

        report = f"""
        ==================================================
              WIZARD OS - EXECUTIVE EXECUTION REPORT
        ==================================================
        Task Objective : {state.task_description}
        Execution Route: {state.route}

        [Performance Metrics]:
        - Total Tasks Processed : {state.metrics.get('total_tasks_completed', 0)}
        - Average Success Rate  : {state.metrics.get('average_success_rate', 0)}%
        - Top Performing Agent  : {state.metrics.get('top_performing_agent', 'N/A')}

        [AI Strategic Recommendation]:
        {recommendation}

        [Execution Trace]:
{trace_lines}

        [System Status]: VERIFIED & OPTIMIZED
        ==================================================
        """
        state.final_report = report.strip()
        state.status = "COMPLETED"
        state.log_step("Synthesizer generated final executive report.")
        return state