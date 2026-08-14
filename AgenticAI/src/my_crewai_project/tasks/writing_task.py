from ..lib import Task


def create_writing_task(tasks_config: dict, writer, analysis_task: Task) -> Task:
    cfg = tasks_config.get("writing_task", {}) if tasks_config else {}
    return Task(description=cfg.get("description", "Write report on {topic}"), expected_output=cfg.get("expected_output"), agent=writer, context=[analysis_task], output_file=cfg.get("output_file"))
