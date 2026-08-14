from ..lib import Agent


def create_writer(agents_config: dict) -> Agent:
    cfg = agents_config.get("writer", {}) if agents_config else {}
    return Agent(config=cfg, tools=[], verbose=True, llm_provider="gemini")
