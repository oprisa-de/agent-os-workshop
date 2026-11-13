import json
import os
from dataclasses import asdict
from datetime import datetime
from typing import Dict
from agents.state import AgentState
from utils.logger import get_logger

logger = get_logger("WizardExporter")


def export_report(state: AgentState, output_dir: str = "exports") -> Dict[str, str]:
    """Exports the completed AgentState into Markdown (.md) and JSON (.json) files."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    md_path = os.path.join(output_dir, f"wizard_report_{timestamp}.md")
    json_path = os.path.join(output_dir, f"wizard_report_{timestamp}.json")

    # 1. Write structured Markdown report
    trace_md = "\n".join([f"- {step}" for step in state.execution_history])
    md_content = f"""# Wizard OS - Executive Execution Report

- **Timestamp:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Task Objective:** {state.task_description}
- **Execution Route:** `{state.route}`
- **Final Status:** `{state.status}`

## Performance Metrics
- **Total Tasks Processed:** {state.metrics.get('total_tasks_completed', 0)}
- **Average Success Rate:** {state.metrics.get('average_success_rate', 0)}%
- **Top Performing Agent:** {state.metrics.get('top_performing_agent', 'N/A')}

## Execution Trace
{trace_md}
"""
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    # 2. Write structured JSON payload (data serialization)
    payload = {
        "generated_at": datetime.now().isoformat(),
        "state": asdict(state)
    }
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(payload, json_file, indent=4, ensure_ascii=False)

    logger.info(f"Reports exported successfully -> MD: '{md_path}' | JSON: '{json_path}'")
    return {"markdown_path": md_path, "json_path": json_path}