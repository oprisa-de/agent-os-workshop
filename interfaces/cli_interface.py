from typing import Callable
from database.db import init_db, fetch_recent_runs


class WizardCLI:
    """Interactive Command-Line Interface for Wizard OS."""

    def __init__(self, workflow_runner: Callable[[str], None]):
        self.workflow_runner = workflow_runner

    def display_banner(self) -> None:
        print("\n" + "=" * 54)
        print("        WIZARD OS - MULTI-AGENT CONTROL PANEL")
        print("=" * 54)

    def show_history(self) -> None:
        runs = fetch_recent_runs(limit=5)
        print("\n--- RECENT WORKFLOW EXECUTIONS (SQLite) ---")
        if not runs:
            print("No execution records found in database yet.")
            return

        for run in runs:
            run_id, ts, task, status, total_tasks, rate, top_agent = run
            print(
                f"#{run_id} | {ts} | Status: {status} | "
                f"Tasks: {total_tasks} | Top: {top_agent} | Task: {task[:40]}..."
            )
        print("-" * 54)

    def start(self) -> None:
        init_db()
        self.display_banner()

        while True:
            print("\nSelect an action:")
            print("  [1] Run multi-agent workflow (Custom or Default task)")
            print("  [2] View recent execution history (SQLite)")
            print("  [3] Exit")

            choice = input("\nEnter choice (1-3): ").strip()

            if choice == "1":
                custom_task = input(
                    "Enter task objective (or press Enter for default): "
                ).strip()
                task = (
                    custom_task
                    if custom_task
                    else "Generate the daily performance report and run advanced analytics on active agents."
                )
                print()
                self.workflow_runner(task)
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                print("\nShutting down Wizard OS. Goodbye!")
                break
            else:
                print("Invalid option. Please enter 1, 2, or 3.")