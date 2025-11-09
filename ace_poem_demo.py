#!/usr/bin/env python3
"""
ace_poem_demo.py

Run ace_print‑style prompts against Tang poems using the latest Google Gemma model.

Usage:
    python ace_poem_demo.py -p [--out-dir /path/to/out]
    python ace_poem_demo.py -s [--out-dir /path/to/out]
"""

import argparse
import os
import sys
from pathlib import Path

# --------------------------------------------------------------
# Google Generative AI SDK
# --------------------------------------------------------------
try:
    import google.generativeai as genai
except ImportError:
    print(
        "Error: google-generativeai SDK not installed. Run `pip install google-generativeai`.",
        file=sys.stderr,
    )
    sys.exit(1)

# --------------------------------------------------------------
# Configuration
# --------------------------------------------------------------
GEMMA_MODEL = "gemma-3-27b-it"   # latest Gemma as of now

# --------------------------------------------------------------
# Prompt generation
# --------------------------------------------------------------
def complex_prompt() -> str:
    system = (
        "You are an expert translator of Tang Dynasty poetry (Du Fu, Li Bai). "
        "Your goal is to create translations that are poetically powerful in English "
        "while remaining faithful to the original's tone, imagery, and meaning."
    )
    playbook = (
        "PROCESS STRATEGIES (learned from previous critiques):\n"
        "Important!  please follow process strategies and note in comments that you applied them"
        "1. Prioritize conciseness and elegance, especially when implying emotional or physical states, "
        "rather than literal descriptions.\n"
        "2. Strive for vivid and evocative imagery, paying close attention to the precise nuance of verbs "
        "to convey atmosphere and emotional depth.\n"
        "3. Prioritize natural English phrasing and rhythm, even if it requires rephrasing literal constructions.\n"
        "4. Ensure interpretations of nuanced or abstract lines directly convey the intended meaning and "
        "integrate smoothly into the overall text, avoiding overly abstract or clunky phrasing.\n"
        "5. When translating descriptions of natural phenomena or personal experience, prioritize strong, "
        "active verbs that convey dynamism and intensity.\n"
        "6. For lines describing sensory experiences or concluding statements, aim for conciseness and "
        "vivid, impactful imagery, even if it requires a less literal approach."
    )
    return f"--- SYSTEM PROMPT ---\n{system}\n\n--- PLAYBOOK (for next run) ---\n{playbook}\n\n--- INPUT ---\n"

def simple_prompt() -> str:
    title = "Simple prompt:  \n"
    instruction = (
        "Translate the following Tang Dynasty poem into English, preserving its meaning, tone, "
        "and poetic style. Keep the translation concise and natural."
    )
    return f"{title}{instruction}\n\n--- INPUT ---\n"

# --------------------------------------------------------------
# File utilities
# --------------------------------------------------------------
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Failed to read {path}: {e}", file=sys.stderr)
        return ""

def write_text(path: Path, content: str):
    try:
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"Failed to write {path}: {e}", file=sys.stderr)

# --------------------------------------------------------------
# Model interaction
# --------------------------------------------------------------
def translate(prompt: str, poem: str) -> str:
    genai.configure(api_key=os.getenv("GAI_API_KEY"))
    model = genai.GenerativeModel(GEMMA_MODEL)
    try:
        response = model.generate_content([prompt, poem])
        return response.text.strip()
    except Exception as e:
        print(f"Model call failed: {e}", file=sys.stderr)
        return ""

# --------------------------------------------------------------
# Main processing
# --------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Translate Tang poems with the latest Gemma model."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", action="store_true", help="Use complex prompt")
    group.add_argument("-s", action="store_true", help="Use simple prompt")
    parser.add_argument(
        "--out-dir",
        default="./output",
        help="Directory where translation files will be written (default: ./output)",
    )
    args = parser.parse_args()

    # Choose prompt
    prompt = complex_prompt() if args.p else simple_prompt()
    mode = "ace" if args.p else "simple"

    # Locate poem files
    data_dir = Path("./data")
    if not data_dir.is_dir():
        print("Error: ./data directory does not exist.", file=sys.stderr)
        sys.exit(1)

    poem_files = sorted(data_dir.glob("tang*.txt"))
    if not poem_files:
        print("Error: No tang*.txt files found in ./data.", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Process each file
    for poem_path in poem_files:
        poem = read_text(poem_path)
        if not poem:
            continue
        translation = translate(prompt, poem)
        if not translation:
            continue

        # Build output file name according to the requested convention
        if mode == "simple":
            out_file = out_dir / f"{poem_path.stem}._simple.txt"
        else:  # complex prompt
            out_file = out_dir / f"{poem_path.stem}_ace.txt"

        write_text(out_file, translation)
        print(f"✔️  {mode} translation written to {out_file}")

if __name__ == "__main__":
    main()

