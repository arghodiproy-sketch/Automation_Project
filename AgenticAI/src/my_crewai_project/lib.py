from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Dict
import os


class Process(Enum):
    sequential = "sequential"
    hierarchical = "hierarchical"


@dataclass
class Agent:
    config: Dict[str, Any] | None = None
    tools: List[Any] = field(default_factory=list)
    verbose: bool = False
    llm_provider: str = "gemini"   # "gemini" | "groq" | "openai"
    model_name: str | None = None  # overrides env default when set

    def _system_prompt(self) -> str:
        if not self.config:
            return "You are a helpful AI assistant."
        role = self.config.get("role", "AI assistant")
        goal = self.config.get("goal", "")
        backstory = self.config.get("backstory", "")
        return (
            f"You are a {role}.\n"
            f"Your goal: {goal}\n"
            f"Background: {backstory}"
        )

    def act(self, prompt: str) -> str:
        role_label = (self.config or {}).get("role", self.llm_provider)
        if self.verbose:
            print(f"\n[{role_label}] ({self.llm_provider}) thinking ...")
        try:
            if self.llm_provider == "gemini":
                return self._act_gemini(prompt)
            if self.llm_provider == "groq":
                return self._act_groq(prompt)
            if self.llm_provider == "openai":
                return self._act_openai(prompt)
        except Exception as exc:
            if self.verbose:
                print(f"  [{self.llm_provider}] ERROR: {exc}")
            return f"[{self.llm_provider} error] {exc}"
        return f"[no provider] {prompt}"

    # ------------------------------------------------------------------ #
    # Gemini via google-genai                                              #
    # ------------------------------------------------------------------ #
    def _act_gemini(self, prompt: str) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in .env")
        try:
            from google import genai
        except ImportError:
            raise ImportError("Run: pip install google-genai")
        client = genai.Client(api_key=api_key)
        model = self.model_name or os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash")
        full_prompt = f"{self._system_prompt()}\n\n{prompt}"
        response = client.models.generate_content(model=model, contents=full_prompt)
        return response.text

    # ------------------------------------------------------------------ #
    # Groq (OpenAI-compatible)                                             #
    # ------------------------------------------------------------------ #
    def _act_groq(self, prompt: str) -> str:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in .env")
        try:
            from groq import Groq
        except ImportError:
            raise ImportError("Run: pip install groq")
        client = Groq(api_key=api_key)
        model = self.model_name or os.environ.get("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1024,
        )
        return resp.choices[0].message.content

    # ------------------------------------------------------------------ #
    # OpenAI fallback                                                      #
    # ------------------------------------------------------------------ #
    def _act_openai(self, prompt: str) -> str:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in .env")
        import openai as _openai
        _openai.api_key = api_key
        model = self.model_name or os.environ.get("OPENAI_MODEL_NAME", "gpt-4o-mini")
        resp = _openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
        )
        return resp["choices"][0]["message"]["content"]


@dataclass
class Task:
    description: str = ""
    expected_output: str | None = None
    agent: Agent | None = None
    context: List[Any] = field(default_factory=list)
    output_file: str | None = None

    def run(self, inputs: Dict[str, Any] | None = None) -> str:
        prompt = self.description
        if inputs:
            try:
                prompt = prompt.format(**inputs)
            except Exception:
                pass
        if self.agent:
            result = self.agent.act(prompt)
        else:
            result = prompt

        # If an output file is specified, persist the result.
        if self.output_file:
            try:
                os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            except Exception:
                # directory creation may fail if path is empty
                pass
            try:
                with open(self.output_file, "w", encoding="utf-8") as f:
                    f.write(result)
            except Exception:
                # ignore write errors in simple scaffold
                if self.agent and self.agent.verbose:
                    print(f"Failed to write output to {self.output_file}")

        return result


@dataclass
class Crew:
    agents: List[Agent] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    process: Process = Process.sequential
    verbose: bool = False

    def kickoff(self, inputs: Dict[str, Any] | None = None) -> str:
        outputs = []
        for task in self.tasks:
            if self.verbose:
                print(f"Running task: {task.description}")
            result = task.run(inputs)
            outputs.append(result)
        return "\n\n".join(outputs)
