#!/usr/bin/env python3
import sys
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv not installed or .env missing; continue without loading
    pass

from .crew import MyCrewAIProject

def run():
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Generative AI in 2025"
    print(f"\n{'='*60}")
    print(f" Starting Crew for topic: {topic}")
    print(f"{'='*60}\n")
    result = MyCrewAIProject().crew().kickoff(inputs={"topic": topic})
    print(f"\n{'='*60}")
    print(" Crew Finished")
    print(f"{'='*60}\n")
    print(result)


if __name__ == "__main__":
    run()
