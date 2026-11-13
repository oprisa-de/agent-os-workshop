import json
import os
import tempfile
import unittest

from agents.analyst import WizardAnalyst
from agents.orchestrator import WizardOrchestrator
from agents.state import AgentState
from agents.synthesizer import WizardSynthesizer
from utils.exporter import export_report
from agents.llm_advisor import WizardLLMAdvisor


class TestWizardOSWorkflow(unittest.TestCase):
    """Unit test suite for Wizard OS routing, analytics, synthesis, and export."""

    def test_orchestrator_routes_to_full_analytics(self) -> None:
        orchestrator = WizardOrchestrator()
        state = AgentState(task_description="Generate daily performance analytics report")
        updated_state = orchestrator.route_task(state)

        self.assertEqual(updated_state.route, "FULL_ANALYTICS_PIPELINE")
        self.assertEqual(updated_state.status, "ROUTED_TO_ANALYST")

    def test_orchestrator_routes_to_quick_summary(self) -> None:
        orchestrator = WizardOrchestrator()
        state = AgentState(task_description="Quick system status ping")
        updated_state = orchestrator.route_task(state)

        self.assertEqual(updated_state.route, "QUICK_SUMMARY_PIPELINE")
        self.assertEqual(updated_state.status, "ROUTED_TO_SYNTHESIZER")

    def test_analyst_kpi_calculations(self) -> None:
        analyst = WizardAnalyst()
        state = AgentState(task_description="Run KPI analysis")
        updated_state = analyst.process_and_analyze(state)

        self.assertEqual(updated_state.status, "ANALYSIS_COMPLETED")
        self.assertEqual(updated_state.metrics["total_tasks_completed"], 416)
        self.assertEqual(updated_state.metrics["top_performing_agent"], "Agent_4")
        self.assertAlmostEqual(updated_state.metrics["average_success_rate"], 90.2)

    def test_synthesizer_and_file_export(self) -> None:
        orchestrator = WizardOrchestrator()
        analyst = WizardAnalyst()
        synthesizer = WizardSynthesizer()

        state = AgentState(task_description="Full end-to-end test report")
        state = orchestrator.route_task(state)
        state = analyst.process_and_analyze(state)
        state = synthesizer.generate_executive_report(state)

        self.assertEqual(state.status, "COMPLETED")
        self.assertIn("WIZARD OS - EXECUTIVE EXECUTION REPORT", state.final_report)

    def test_llm_advisor_fallback_recommendations(self) -> None:
        analyst = WizardAnalyst()
        advisor = WizardLLMAdvisor()
        advisor.api_key = ""  # Force offline fallback mode for deterministic testing

        state = AgentState(task_description="Evaluate agent efficiency")
        state = analyst.process_and_analyze(state)
        state = advisor.generate_recommendations(state)

        self.assertIn("Agent_4", state.ai_insights)
        self.assertTrue(len(state.ai_insights) > 20)

        # Verify Markdown and JSON exports using an isolated temporary directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            paths = export_report(state, output_dir=tmp_dir)
            self.assertTrue(os.path.exists(paths["markdown_path"]))
            self.assertTrue(os.path.exists(paths["json_path"]))

            with open(paths["json_path"], "r", encoding="utf-8") as f:
                data = json.load(f)
                self.assertEqual(data["state"]["metrics"]["top_performing_agent"], "Agent_4")


if __name__ == "__main__":
    unittest.main()