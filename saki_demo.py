"""
saki_demo.py

Generate a single satirical story using the latest Google Gemma model.

Usage:
    python saki_demo.py -p   # complex prompt (with PLAYBOOK)
    python saki_demo.py -s   # simple prompt
"""

import argparse
import os
import sys
from pathlib import Path

# ----------------------------------------------------------------------
# Google Generative AI SDK
# ----------------------------------------------------------------------
try:
    import google.generativeai as genai
except ImportError:
    print(
        "Error: google-generativeai SDK not installed. Run `pip install google-generativeai`.",
        file=sys.stderr,
    )
    sys.exit(1)

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
GEMMA_MODEL = "gemma-3-27b-it"   # latest Gemma as of now

# ----------------------------------------------------------------------
# Prompt definitions
# ----------------------------------------------------------------------
def complex_prompt() -> str:
    return """Important!  Follow all strategies in PLAYBOOK and note how you followed them
--- SYSTEM PROMPT ---
You are an expert at creating stories and character development.  Your stories have sharp social satire to mock the superficiality of upper-class society.  Can at times subvert authority and societal norms through the use of mischievous characters, elaborate practical jokes, and a recurring motif of wild nature disrupting artificial human order. Story should blend witty, droll humor with a dark, macabre sensibility that exposes the underlying cruelty and hypocrisy of human nature
--- PLAYBOOK (for next run) ---
PROCESS STRATEGIES (learned from previous critiques):
1. Develop characters with subtle psychological depth and manipulative genius, avoiding overt caricatures.
2. Craft a narrative with masterful misdirection and a shocking, unpredictable twist, rather than explicitly stating the main plot early.
3. Prioritize understated wit and subtle satire over overt critique to reveal character flaws.
4. Develop individual character depth through specific dialogue and interactions, ensuring plot twists and resolutions are character-driven.
5. Avoid explicit exposition or dialogue that explains the story's satirical elements, plot devices, or underlying critique; instead, _show_ these through character actions, unconventional behavior, and understated narration.
6. Integrate humor organically into character behavior and dialogue, developing eccentric and witty characters whose inherent traits and actions drive the narrative's comedic and satirical impact"""

def simple_prompt() -> str:
    return """You are an expert at creating stories and character development.  Your stories have sharp social satire to mock the superficiality of upper-class society.  Can at times subvert authority and societal norms through the use of mischievous characters, elaborate practical jokes, and a recurring motif of wild nature disrupting artificial human order. Story should blend witty, droll humor with a dark, macabre sensibility that exposes the underlying cruelty and hypocrisy of human nature"""

# ----------------------------------------------------------------------
# Model interaction
# ----------------------------------------------------------------------
def generate_story(prompt: str) -> str:
    """Send the prompt to the Gemma model and return the generated story."""
    genai.configure(api_key=os.getenv("GAI_API_KEY"))
    model = genai.GenerativeModel(GEMMA_MODEL)
    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        print(f"Model call failed: {e}", file=sys.stderr)
        return ""

# ----------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate a satirical story using the latest Gemma model."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", action="store_true", help="Use complex prompt (with PLAYBOOK)")
    group.add_argument("-s", action="store_true", help="Use simple prompt")
    args = parser.parse_args()

    prompt = complex_prompt() if args.p else simple_prompt()
    mode = "complex" if args.p else "simple"

    print(f"=== Generating {mode} story ===\n")
    story = generate_story(prompt)
    if story:
        print(story)
    else:
        print("No story was generated.", file=sys.stderr)

if __name__ == "__main__":
    main()
