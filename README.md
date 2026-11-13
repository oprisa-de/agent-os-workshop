# Wizard OS - Multi-Agent AI Orchestration System

A modular Python-based multi-agent framework designed to orchestrate dynamic workflows, process analytical KPIs, persist execution history, and export structured executive reports.

## Key Features
* **Typed State Management (`AgentState`):** Central dataclass tracking task objectives, dynamic routing decisions, metrics, and execution traces across nodes.
* **Dynamic Task Routing:** `WizardOrchestrator` inspects incoming requests and routes them either through the `FULL_ANALYTICS_PIPELINE` or the lightweight `QUICK_SUMMARY_PIPELINE`.
* **Data Analytics Engine:** `WizardAnalyst` leverages `pandas` and `numpy` to compute operational KPIs and identify top-performing agents.
* **Executive Synthesis & Multi-Format Export:** `WizardSynthesizer` and `WizardExporter` compile execution traces into formatted console reports, Markdown (`.md`), and JSON (`.json`) files.
* **SQLite Persistence & Interactive CLI:** Embedded SQLite database (`database/db.py`) paired with an interactive Control Panel (`interfaces/cli_interface.py`) to run workflows and query execution history.
* **Centralized Logging & Unit Tests:** Standardized file/console logging (`utils/logger.py`) and automated unit tests (`tests/test_workflow.py`).

## Tech Stack
* **Language:** Python 3.10+
* **Data & Analytics:** Pandas, NumPy
* **Database:** SQLite3
* **Testing:** `unittest` / `pytest`
* **Architecture:** Modular Multi-Agent Orchestration (LangGraph-inspired state graph)

## Project Structure
```text
agent-os-workshop/
│
├── agents/                 # AgentState, Orchestrator, Analyst, and Synthesizer nodes
├── database/               # SQLite initialization, persistence, and history queries
├── interfaces/             # Interactive CLI Control Panel
├── tests/                  # Automated unit test suite
├── utils/                  # Centralized logging and Markdown/JSON report exporters
├── main.py                 # Core workflow entry point
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation