import pandas as pd
import numpy as np


class WizardAnalyst:
    def __init__(self, name: str):
        self.name = name

    def process_and_analyze(self, data_source: str = "default_metrics") -> dict:
        print(f"[{self.name}] Processing data from source: '{data_source}'...")

        # Simulating performance data for our AI agents or business workflows
        np.random.seed(42)
        mock_data = {
            "agent_id": [f"Agent_{i}" for i in range(1, 6)],
            "tasks_completed": np.random.randint(40, 120, size=5),
            "success_rate": np.random.uniform(0.85, 0.99, size=5).round(2),
            "avg_latency_sec": np.random.uniform(1.2, 4.5, size=5).round(2)
        }

        df = pd.DataFrame(mock_data)

        # Performing basic analytical aggregations
        total_tasks = int(df["tasks_completed"].sum())
        mean_success_rate = float(df["success_rate"].mean())
        best_agent = df.loc[df["success_rate"].idxmax()]["agent_id"]

        analysis_report = {
            "total_tasks_completed": total_tasks,
            "average_success_rate": mean_success_rate,
            "top_performing_agent": best_agent,
            "raw_summary": df.to_dict(orient="records")
        }

        print(f"[{self.name}] Analysis complete. Top performer: {best_agent}")
        return analysis_report


if __name__ == "__main__":
    # Test the analyst agent independently
    analyst_bot = WizardAnalyst(name="Wizard-OS-Analyst")
    report = analyst_bot.process_and_analyze()

    print("\n--- ANALYTICAL REPORT SUMMARY ---")
    print(f"Total Tasks: {report['total_tasks_completed']}")
    print(f"Average Success Rate: {report['average_success_rate'] * 100:.1f}%")
    print(f"Top Agent: {report['top_performing_agent']}")