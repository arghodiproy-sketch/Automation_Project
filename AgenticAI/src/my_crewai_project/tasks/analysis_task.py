from ..lib import Task


def create_analysis_task(tasks_config: dict, analyst, research_task: Task) -> Task:
    cfg = tasks_config.get("analysis_task", {}) if tasks_config else {}
    return Task(description=cfg.get("description", "Analyze research on {topic}"), expected_output=cfg.get("expected_output"), agent=analyst, context=[research_task])
