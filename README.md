# Wizard OS - Multi-Agent AI Orchestration System

A modular Python-based multi-agent framework designed to orchestrate workflows, process analytical data, and maintain persistent state management. Developed as part of an advanced AI Engineering portfolio.

## 🚀 Key Features
* **Multi-Agent Architecture:** Modular separation of core orchestrator and data analysis agents.
* **Data Processing:** Integrated with `pandas` and `numpy` to generate automated performance metrics and KPIs.
* **Database Persistence:** Stores workflow execution history and metrics securely in an embedded SQLite database.
* **Extensible Workflow:** Built with clean, production-ready Python code following enterprise standards.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Libraries:** Pandas, NumPy, LangGraph concepts, Dotenv
* **Database:** SQLite
* **IDE:** PyCharm

## 📁 Project Structure
```text
agent-os-workshop/
│
├── agents/             # Agent logic (Orchestrator, Analyst)
├── database/           # SQLite database persistence layer
├── interfaces/         # External communication channels
├── main.py             # Core execution entry point
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation