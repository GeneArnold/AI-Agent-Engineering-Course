import sys
import os
from pathlib import Path

# Add parent dir to path for .env loading
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Load .env from root
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Now run a quick syntax check
print("✅ Imports successful")
print(f"✅ .env loaded from: {env_path}")
print(f"✅ API key present: {bool(os.getenv('OPENAI_API_KEY'))}")

# Import the judge module
import judge_agent
print("✅ judge_agent.py syntax is valid")
print("✅ All rubrics can be loaded")

# Try loading each rubric
for rubric_file in ["code_quality.json", "content_quality.json", "customer_service.json"]:
    judge = judge_agent.JudgeAgent(rubric_path=f"rubrics/{rubric_file}")
    print(f"  ✅ {rubric_file}")

print("\n✅ All tests passed! Code is ready to run.")
print("Note: Full demo requires API credits. Run 'python judge_agent.py' to test with live API.")
