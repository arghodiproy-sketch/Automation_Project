from ..lib import Agent


def create_analyst(agents_config: dict) -> Agent:
    cfg = agents_config.get("analyst", {}) if agents_config else {}
    return Agent(config=cfg, tools=[], verbose=True, llm_provider="groq")
