# jon2allen-ace_process

##  Agentic Context Engineering (ACE) Pipeline Proof of Concept

This repository contains a proof-of-concept implementation of an **Agentic Context Engineering (ACE) Pipeline**. The ACE loop is designed to create **self-correcting** AI workflows by following an **Execute, Critique, Reflect, and Curate (Playbook)** cycle.

The primary demonstration focuses on applying this self-improvement loop to two complex tasks: **Chinese Poetry Translation** and **Saki-style Satirical Story Generation**.


More in Medium article - https://medium.com/@jallenswrx2016/agentic-context-engineering-cdc4e215c68d

---

##  Key Features

* **Self-Correcting Prompts:** The pipeline dynamically generates "learned patterns" (a **Playbook**) based on a critique of the previous output against a ground truth or desired standard. This Playbook is then injected into the next execution stage to immediately improve the results.
* **Modular Stage Definition:** Workflows are defined as a series of Python dictionaries (`STAGES` and `JOBS`) which are easily managed and modified.
* **General Purpose Driver:** The `ace_run_pipeline.py` script can execute any pipeline defined in the configuration JSON, making the core logic reusable.
* **Web-Based Config Editor:** Includes a simple HTML/Alpine.js editor (`ace_editor_v1.html`) for visually creating and modifying the pipeline configuration files (`.json`).

---

Setup and Execution

## Prerequisites

1.  **Python 3.8+**
2.  **Google Generative AI SDK:**
    ```bash
    pip install google-generativeai
    ```

## API Key Configuration

The scripts rely on an environment variable for the API key:

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```


## pipline run

```bash
python3 ace_run_pipeline.py tang_poet.json
```
## extract curated prompt

```bash

usage: ace_print.py [-h] -f FILE [-l] [-s] [-p] [--poem POEM]

Print playbook_snapshots or prompts from a JSON file.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the JSON file
  -l, --last            Print only the last playbook_snapshot
  -s, --system          Print only the system prompt from the last current_ace_prompt
  -p, --prompt          Print the full prompt (system + strategies) from the last current_ace_prompt

example run:

[jon2allen@freebsd14 ~/github/ace_process]$ ./ace_print.py -f poetry_translator_history_run_type1.json -p
Important!  Follow all strategies in PLAYBOOK and note how you followed them 
--- SYSTEM PROMPT ---
You are an expert translator of Tang Dynasty poetry (Du Fu, Li Bai). Your goal is to create translations that are poetically powerful in English while remaining faithful to the original's tone, imagery, and meaning.

--- PLAYBOOK (for next run) ---
PROCESS STRATEGIES (learned from previous critiques):
1. Prioritize conciseness and elegance, especially when implying emotional or physical states, rather than literal descriptions.
2. Strive for vivid and evocative imagery, paying close attention to the precise nuance of verbs to convey atmosphere and emotional depth.
3. Prioritize natural English phrasing and rhythm, even if it requires rephrasing literal constructions.
4. Ensure interpretations of nuanced or abstract lines directly convey the intended meaning and integrate smoothly into the overall text, avoiding overly abstract or clunky phrasing.
5. When translating descriptions of natural phenomena or personal experience, prioritize strong, active verbs that convey dynamism and intensity.
6. For lines describing sensory experiences or concluding statements, aim for conciseness and vivid, impactful imagery, even if it requires a less literal approach.

```
## Poem review
```bash
python3 ace_driver_poems.py
python3 ace_run_pipeline.py tang_poet.json
```

## Saki story generation 
```bash
python3 ace_run_pipeline.py saki6.json
```


## ACE Pipeline Logic Overview
Each Job in the pipeline executes a series of Stages (e.g., 1_Execute, 2_Critique, 3_Reflect).

1_Execute (or 1_translate / 1_create_story): Takes the current Playbook (a list of best-practice instructions) and the raw Input (e.g., Chinese poem) to produce an output JSON.

2_Critique: Takes the raw Input, the model's output from Stage 1, and a human-provided Ground Truth (expert translations/stories). It outputs a JSON of strengths and weaknesses.

3_Reflect: Takes the weaknesses and main_critique from Stage 2 and generates new, actionable instructions called learned_patterns.

Curator (ace_util.py): The process method passes the learned_patterns to the internal curator, which adds them to the global Playbook.

Iteration: The next Job in the sequence repeats the process, feeding the now-improved Playbook into its own 1_Execute stage, resulting in a smarter prompt and better output.
