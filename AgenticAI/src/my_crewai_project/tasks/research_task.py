from ..lib import Task


def create_research_task(tasks_config: dict, researcher) -> Task:
    cfg = tasks_config.get("research_task", {}) if tasks_config else {}
    return Task(description=cfg.get("description", "Research {topic}"), expected_output=cfg.get("expected_output"), agent=researcher)
