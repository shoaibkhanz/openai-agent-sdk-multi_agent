from pathlib import Path
import openai

ROOT = Path(__file__).parents[1]
TRANSACTIONS_PATH = ROOT / "data" / "financial_transactions.json"
PDF_PATH = ROOT / "data" / "build-wealth.pdf"

CLIENT = openai.OpenAI(project="proj_DEb1OlP06KoUF2Qi8geIGnk4")
