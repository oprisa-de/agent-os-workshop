import pandas as pd
import numpy as np
from agents.state import AgentState
from utils.logger import get_logger

logger = get_logger("WizardAnalyst")


class WizardAnalyst:
    """Data processing agent utilizing Pandas and NumPy for KPI extraction."""

    def __init__(self, name: str = "Wizard-OS-Analyst"):
        self.name = name

    def process_and_analyze(self, state: AgentState, data_source: str = "agent_performance_logs") -> AgentState:
        """Processes operational logs and populates analytical KPIs into AgentState."""
        logger.info(f"[{self.name}] Processing data from source: '{data_source}'...")

        # Simulated structured agent telemetry dataset
        data = {
            "agent_id": ["Agent_1", "Agent_2", "Agent_3", "Agent_4", "Agent_5"],
            "tasks_completed": [78, 84, 69, 102, 83],
            "success_rate": [88.5, 91.2, 84.0, 96.8, 90.5]
        }
        df = pd.DataFrame(data)

        total_tasks = int(df["tasks_completed"].sum())
        avg_success_rate = round(float(np.mean(df["success_rate"])), 2)
        top_agent = str(df.loc[df["tasks_completed"].idxmax(), "agent_id"])

        state.metrics = {
            "data_source": data_source,
            "total_tasks_completed": total_tasks,
            "average_success_rate": avg_success_rate,
            "top_performing_agent": top_agent
        }
        state.status = "ANALYSIS_COMPLETED"
        state.log_step(f"Analyst processed {total_tasks} tasks (Top agent: {top_agent}).")

        logger.info(
            f"[{self.name}] Analysis complete. Tasks: {total_tasks} | "
            f"Avg Success: {avg_success_rate}% | Top: {top_agent}"
        )
        return state