import json
import os
from gemini_client import analyze_pdf
from prompts import EXTRACTION_PROMPT

PDF_PATH = "samples/LawsOfChess.pdf"
OUTPUT_DIR = "outputs"
OUTPUT_FILE = "outputs/chess_rules_extraction.json"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    result = analyze_pdf(PDF_PATH, EXTRACTION_PROMPT)

    parsed = json.loads(result)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)

    print(f"\nExtraction saved to: {OUTPUT_FILE}\n")
    print(json.dumps(parsed, indent=2))


if __name__ == "__main__":
    main()