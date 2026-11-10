import os
from typing import TypedDict, List
from dotenv import load_dotenv

load_dotenv()


# Define the state tracked by the agent (State management using LangGraph / Core System)
class AgentState(TypedDict):
    task_description: str
    decisions_needed: List[str]
    status: str
    output_report: str


class WizardOrchestrator:
    def __init__(self, name: str):
        self.name = name

    def analyze_task(self, task: str) -> AgentState:
        print(f"[{self.name}] Analyzing incoming task: '{task}'...")

        # Simulating the logic where the agent identifies missing decisions or parameters
        state = AgentState(
            task_description=task,
            decisions_needed=[
                "At what time should the report be sent and in which timezone?",
                "Which KPIs or data columns should be tracked automatically?",
                "Confirmation of permissions for databases or external files."
            ],
            status="WAITING_FOR_USER_INPUT",
            output_report=""
        )
        return state


if __name__ == "__main__":
    # Quick test of the orchestrator directly inside PyCharm
    bot = WizardOrchestrator(name="Wizard-OS-Core")
    current_state = bot.analyze_task("Generate the daily performance report for active agents.")

    print("\n--- CURRENT AGENT STATE ---")
    print(f"Status: {current_state['status']}")
    print("Decisions required from user:")
    for i, decision in enumerate(current_state['decisions_needed'], 1):
        print(f"  {i}. {decision}")