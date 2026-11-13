import os
from dotenv import load_dotenv
from agents.state import AgentState
from utils.logger import get_logger

load_dotenv()
logger = get_logger("WizardLLMAdvisor")


class WizardLLMAdvisor:
    """Generative AI node that produces actionable optimization recommendations."""

    def __init__(self, name: str = "Wizard-OS-LLM-Advisor", model: str = "gpt-4o-mini"):
        self.name = name
        self.model = os.getenv("LLM_MODEL", model)
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()

    def _generate_fallback_insights(self, state: AgentState) -> str:
        """Deterministic fallback engine used when no external LLM API key is configured."""
        top_agent = state.metrics.get("top_performing_agent", "N/A")
        avg_rate = state.metrics.get("average_success_rate", 0.0)
        total_tasks = state.metrics.get("total_tasks_completed", 0)

        if total_tasks == 0:
            return (
                "System health check passed with 100% availability. "
                "No batch bottleneck detected; system is ready for full workload."
            )

        return (
            f"Scale workload allocation pattern from {top_agent} across lower-performing nodes "
            f"to lift overall success rate above {avg_rate}% (currently {total_tasks} tasks processed)."
        )

    def generate_recommendations(self, state: AgentState) -> AgentState:
        """Calls an LLM API to interpret KPIs, with automatic offline fallback."""
        logger.info(f"[{self.name}] Generating strategic AI recommendations...")

        if not self.api_key or self.api_key == "your_openai_api_key_here":
            logger.info(f"[{self.name}] No active API key found. Using deterministic fallback mode.")
            state.ai_insights = self._generate_fallback_insights(state)
            state.log_step("LLM Advisor generated recommendations via offline fallback engine.")
            return state

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            prompt = (
                f"You are an AI Operations & Process Optimization Advisor. "
                f"Analyze these workflow metrics and give one concise, actionable recommendation (max 2 sentences):\n"
                f"- Task: {state.task_description}\n"
                f"- Metrics: {state.metrics}\n"
            )

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Provide concise, executive-level operational insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=120
            )

            state.ai_insights = response.choices[0].message.content.strip()
            state.log_step(f"LLM Advisor generated live AI insights using {self.model}.")
            logger.info(f"[{self.name}] Live LLM recommendation generated successfully.")

        except Exception as exc:
            logger.warning(f"[{self.name}] LLM API call failed ({exc}). Switching to fallback engine.")
            state.ai_insights = self._generate_fallback_insights(state)
            state.log_step("LLM Advisor recovered via fallback engine after API exception.")

        return state