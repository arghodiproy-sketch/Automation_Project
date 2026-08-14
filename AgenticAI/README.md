# my_crewai_project

Scaffolded CrewAI example project created from the provided implementation guide.

Quick start (Windows PowerShell):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. (Optional) Create a `.env` from `.env.example` and set `OPENAI_API_KEY`.

4. Run the project (ensure `src` is on `PYTHONPATH`):

```powershell
$env:PYTHONPATH = 'src'
python -m my_crewai_project.main "Generative AI in 2025"
```

Or run without setting `PYTHONPATH` by adding `src` at runtime:

```powershell
python -c "import sys; sys.path.insert(0,'src'); from my_crewai_project.main import run; run()"
```

Tests:

```powershell
pip install pytest
python -m pytest tests/test_smoke.py -q
```

Notes:
- The scaffold includes a minimal local `lib.py` so you can run without the
	external `crewai` package. To use real CrewAI, replace `lib.py` with the
	upstream implementations and install the package.
- If you provide `OPENAI_API_KEY` in `.env`, agents will call OpenAI.

