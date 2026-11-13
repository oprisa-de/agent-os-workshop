from agents.orchestrator import WizardOrchestrator
from agents.analyst import WizardAnalyst
from agents.synthesizer import WizardSynthesizer
from database.db import init_db, save_task_run
from interfaces.cli_interface import WizardCLI


def run_agent_workflow(user_task: str) -> None:
    print("=== STARTING WIZARD OS MULTI-AGENT WORKFLOW ===\n")

    # 0. Ensure the database is initialized
    init_db()

    # 1. Initialize the Orchestrator Agent
    orchestrator = WizardOrchestrator(name="Wizard-OS-Core")
    initial_state = orchestrator.analyze_task(user_task)

    print(f"\n[Status]: {initial_state['status']}")
    print("[Orchestrator Action]: Requirements validated. Handing over to Analyst Agent...\n")

    # 2. Initialize the Analyst Agent and execute data processing
    analyst = WizardAnalyst(name="Wizard-OS-Analyst")
    analysis_results = analyst.process_and_analyze(data_source="agent_performance_logs")

    # 3. Initialize the Synthesizer Agent to format the final executive report
    synthesizer = WizardSynthesizer(name="Wizard-OS-Synthesizer")
    executive_report = synthesizer.generate_executive_report(
        task_description=initial_state["task_description"],
        metrics=analysis_results
    )

    print("\n" + executive_report + "\n")

    # 4. Persist results to SQLite database
    save_task_run(
        task_description=initial_state["task_description"],
        status="COMPLETED",
        total_tasks=analysis_results["total_tasks_completed"],
        avg_success_rate=analysis_results["average_success_rate"],
        top_agent=analysis_results["top_performing_agent"]
    )

    print("\n=== WORKFLOW FINISHED & SAVED SUCCESSFULLY ===")


if __name__ == "__main__":
    cli = WizardCLI(workflow_runner=run_agent_workflow)
    cli.start()