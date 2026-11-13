from agents.orchestrator import WizardOrchestrator
from agents.analyst import WizardAnalyst
from agents.synthesizer import WizardSynthesizer
from database.db import init_db, save_task_run


def run_agent_workflow(user_task: str):
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

    # Print the formatted report in console
    print("\n" + executive_report + "\n")

    # 4. Extract metrics for database persistence
    status_completed = "COMPLETED"
    total_tasks = analysis_results['total_tasks_completed']
    avg_success = analysis_results['average_success_rate']
    top_agent = analysis_results['top_performing_agent']

    # 5. Persist results to SQLite database
    save_task_run(
        task_description=initial_state["task_description"],
        status=status_completed,
        total_tasks=total_tasks,
        avg_success_rate=avg_success,
        top_agent=top_agent
    )

    print("\n=== WORKFLOW FINISHED & SAVED SUCCESSFULLY ===")


if __name__ == "__main__":
    sample_task = "Generate the daily performance report and run advanced analytics on active agents."
    run_agent_workflow(sample_task)