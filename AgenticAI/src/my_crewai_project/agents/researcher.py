from ..lib import Agent
from ..tools.search_tool import web_search


class ResearcherAgent(Agent):
    def act(self, prompt: str) -> str:
        # Use web_search as a simple tool to enrich responses
        search_results = web_search(prompt)
        if self.verbose:
            print(f"[Researcher] search results: {search_results}")
        base = super().act(prompt)
        return f"{base}\n\nSearch:\n{search_results}"


def create_researcher(agents_config: dict) -> Agent:
    cfg = agents_config.get("researcher", {}) if agents_config else {}
    return ResearcherAgent(config=cfg, tools=[web_search], verbose=True, llm_provider="groq")
