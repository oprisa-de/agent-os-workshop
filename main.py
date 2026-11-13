from agents.state import AgentState
from agents.orchestrator import WizardOrchestrator
from agents.analyst import WizardAnalyst
from agents.llm_advisor import WizardLLMAdvisor
from agents.synthesizer import WizardSynthesizer
from database.db import init_db, save_task_run
from interfaces.cli_interface import WizardCLI
from utils.exporter import export_report
from utils.logger import get_logger

logger = get_logger("WizardMain")


def run_agent_workflow(user_task: str) -> None:
    logger.info("=== STARTING WIZARD OS MULTI-AGENT WORKFLOW ===")

    # 0. Initialize persistence layer and shared AgentState
    init_db()
    state = AgentState(task_description=user_task)

    # 1. Orchestrator classifies and routes the state
    orchestrator = WizardOrchestrator(name="Wizard-OS-Core")
    state = orchestrator.route_task(state)

    # 2. Conditional execution based on dynamic routing
    if state.route == "FULL_ANALYTICS_PIPELINE":
        analyst = WizardAnalyst(name="Wizard-OS-Analyst")
        state = analyst.process_and_analyze(state, data_source="agent_performance_logs")
    else:
        logger.info("[Workflow] Skipping Analyst node per QUICK_SUMMARY_PIPELINE route.")

    # 3. LLM Advisor generates strategic recommendations
    advisor = WizardLLMAdvisor(name="Wizard-OS-LLM-Advisor")
    state = advisor.generate_recommendations(state)

    # 4. Synthesizer compiles the final report from AgentState
    synthesizer = WizardSynthesizer(name="Wizard-OS-Synthesizer")
    state = synthesizer.generate_executive_report(state)

    print("\n" + state.final_report + "\n")

    # 5. Persist execution state to SQLite
    save_task_run(
        task_description=state.task_description,
        status=state.status,
        total_tasks=state.metrics.get("total_tasks_completed", 0),
        avg_success_rate=state.metrics.get("average_success_rate", 0.0),
        top_agent=state.metrics.get("top_performing_agent", "N/A")
    )

    # 6. Export structured reports to Markdown and JSON
    exported_files = export_report(state)
    print(f"[Export] Markdown report saved to: {exported_files['markdown_path']}")
    print(f"[Export] JSON report saved to    : {exported_files['json_path']}")

    logger.info("=== WORKFLOW FINISHED & SAVED SUCCESSFULLY ===")


if __name__ == "__main__":
    cli = WizardCLI(workflow_runner=run_agent_workflow)
    cli.start()