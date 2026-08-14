import yaml
from pathlib import Path
from .lib import Crew, Process


def _load_config(filename: str) -> dict:
    # Try package-local config (src/config/) then repo-root config (../config/)
    candidates = [
        Path(__file__).parent.parent / "config" / filename,
        Path(__file__).parent.parent.parent / "config" / filename,
    ]
    for config_path in candidates:
        if config_path.exists():
            with open(config_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
    return {}


class MyCrewAIProject:
    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    def __init__(self):
        self._agents_config = _load_config(self.agents_config) or {}
        self._tasks_config = _load_config(self.tasks_config) or {}

    # -- Agents --------------------------------------------------------------
    def researcher(self):
        from .agents.researcher import create_researcher

        return create_researcher(self._agents_config)

    def analyst(self):
        from .agents.analyst import create_analyst

        return create_analyst(self._agents_config)

    def writer(self):
        from .agents.writer import create_writer

        return create_writer(self._agents_config)

    # -- Tasks ----------------------------------------------------------------
    def research_task(self):
        from .tasks.research_task import create_research_task

        return create_research_task(self._tasks_config, self.researcher())

    def analysis_task(self):
        from .tasks.analysis_task import create_analysis_task

        return create_analysis_task(self._tasks_config, self.analyst(), self.research_task())

    def writing_task(self):
        from .tasks.writing_task import create_writing_task

        return create_writing_task(self._tasks_config, self.writer(), self.analysis_task())

    # -- Crew -----------------------------------------------------------------
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.analyst(), self.writer()],
            tasks=[self.research_task(), self.analysis_task(), self.writing_task()],
            process=Process.sequential,
            verbose=True,
        )
