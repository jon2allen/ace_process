# jon2allen-ace_process

## 🎯 Agentic Context Engineering (ACE) Pipeline Proof of Concept

This repository contains a proof-of-concept implementation of an **Agentic Context Engineering (ACE) Pipeline**. The ACE loop is designed to create **self-correcting** AI workflows by following an **Execute, Critique, Reflect, and Curate (Playbook)** cycle.

The primary demonstration focuses on applying this self-improvement loop to two complex tasks: **Chinese Poetry Translation** and **Saki-style Satirical Story Generation**.

---

## 🚀 Key Features

* **Self-Correcting Prompts:** The pipeline dynamically generates "learned patterns" (a **Playbook**) based on a critique of the previous output against a ground truth or desired standard. This Playbook is then injected into the next execution stage to immediately improve the results.
* **Modular Stage Definition:** Workflows are defined as a series of Python dictionaries (`STAGES` and `JOBS`) which are easily managed and modified.
* **General Purpose Driver:** The `ace_run_pipeline.py` script can execute any pipeline defined in the configuration JSON, making the core logic reusable.
* **Web-Based Config Editor:** Includes a simple HTML/Alpine.js editor (`ace_editor_v1.html`) for visually creating and modifying the pipeline configuration files (`.json`).

---

Setup and Execution

### Prerequisites

1.  **Python 3.8+**
2.  **Google Generative AI SDK:**
    ```bash
    pip install google-generativeai
    ```

### API Key Configuration

The scripts rely on an environment variable for the API key:

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"


##$ Poem review
python3 ace_driver_poems.py
# Or, using the generic runner with the config file:
python3 ace_run_pipeline.py tang_poet.json

### Saki story generation 
python3 ace_run_pipeline.py saki6.json



Here is the README in raw markdown format for the jon2allen-ace_process repository.

Markdown

# 🤖 jon2allen-ace_process

## 🎯 Agentic Context Engineering (ACE) Pipeline Proof of Concept

This repository contains a proof-of-concept implementation of an **Agentic Context Engineering (ACE) Pipeline**. The ACE loop is designed to create **self-correcting** AI workflows by following an **Execute, Critique, Reflect, and Curate (Playbook)** cycle.

The primary demonstration focuses on applying this self-improvement loop to two complex tasks: **Chinese Poetry Translation** and **Saki-style Satirical Story Generation**.

---

## 🚀 Key Features

* **Self-Correcting Prompts:** The pipeline dynamically generates "learned patterns" (a **Playbook**) based on a critique of the previous output against a ground truth or desired standard. This Playbook is then injected into the next execution stage to immediately improve the results.
* **Modular Stage Definition:** Workflows are defined as a series of Python dictionaries (`STAGES` and `JOBS`) which are easily managed and modified.
* **General Purpose Driver:** The `ace_run_pipeline.py` script can execute any pipeline defined in the configuration JSON, making the core logic reusable.
* **Web-Based Config Editor:** Includes a simple HTML/Alpine.js editor (`ace_editor_v1.html`) for visually creating and modifying the pipeline configuration files (`.json`).

---

## 📁 Repository Structure

└── jon2allen-ace_process/     ├── README.md     ├── LICENSE         ├── ace_util.py # 🛠️ Core logic: AcePipeline class with _call_llm, curator, and process loop.     ├── ace_run_pipeline.py # 🏃 General script to load a config JSON (STAGES/JOBS) and run the ACE pipeline.     ├── ace_driver_poems.py # 🧪 Concrete pipeline example: Chinese Poetry Translator (Du Fu).     ├── ace_driver_poems1.py # 🧪 Concrete pipeline example: Du Fu Translation Style Analysis.     ├── ace_poem_demo.py # 💡 Simple demo for direct model comparison (ACE vs. Simple prompt) on Chinese poems.     ├── ace_print.py # 🖨️ Utility script to pretty-print the final playbook/prompt from a history file.     ├── ace_editor_v1.html # ⚙️ Alpine.js / Tailwind CSS web editor for creating STAGES/JOBS JSON configs.         ├── tang_poet.json # ⚙️ Config file for the Du Fu translation pipeline.     ├── saki6.json # ⚙️ Config file for the Saki-style story generation pipeline.         ├── poetry_translator_history_run_type1.json # 💾 Sample run history for the translation pipeline.     ├── sample_poetry_analysis_history_run.json # 💾 Sample run history for the analysis pipeline.         ├── sample_run_0.txt # 📝 Terminal output example: ace_driver_poems.py run.     ├── sample_run.txt # 📝 Terminal output example: ace_driver_poems1.py run.         ├── saki_demo.py # 💡 Simple demo for direct model comparison (ACE vs. Simple prompt) on Saki story generation.     ├── saki_out_playbook_prompt.txt # 📝 Sample story output using the complex, learned prompt.     ├── saki_out_standard_prompt.txt # 📝 Sample story output using the simple prompt.         ├── data/ # 📚 Directory containing input data (Tang Dynasty poems).     │   └── tangXX_poem.txt

    └── saki/ # 📚 Directory containing ground truth stories (Saki's works).         ├── method.txt         ├── open_window.txt         └── tiger.txt


---

## 🛠️ Setup and Execution

### Prerequisites

1.  **Python 3.8+**
2.  **Google Generative AI SDK:**
    ```bash
    pip install google-generativeai
    ```

### API Key Configuration

The scripts rely on an environment variable for the API key:

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
Running the Pipelines
You can run a specific, hardcoded driver script or use the general runner with a config file.

1. Poetry Translation (Self-Correction Demo)
This runs three poems sequentially, with each subsequent translation benefiting from the learned_patterns added to the Playbook by the critique stage of the previous poem.

Bash

python3 ace_driver_poems.py
# Or, using the generic runner with the config file:
python3 ace_run_pipeline.py tang_poet.json
2. Saki Story Generation
This uses a complex config (saki6.json) to analyze sample Saki stories, extract principles of good satire, and generate a final set of rules for creative writing.

Bash

python3 ace_run_pipeline.py saki6.json
Running the Demos (Prompt Comparison)
These scripts compare a simple, static prompt against a robust, learned prompt (like the one generated by a full ACE run) for quality comparison.

Bash

# Compare simple vs. ACE prompt for a Saki-style story
python3 saki_demo.py -s # Simple prompt
python3 saki_demo.py -p # Complex (Playbook) prompt

# Compare simple vs. ACE prompt for Tang poetry translation
python3 ace_poem_demo.py -s # Simple prompt
python3 ace_poem_demo.py -p # Complex (Playbook) prompt
Utility: Printing the Final Playbook
To see the final instructions generated after a successful run:

Bash

# Print the final playbook/prompt from the last run in the history file
python3 ace_print.py -f poetry_translator_history.json -p


# ACE Pipeline Logic Overview
Each Job in the pipeline executes a series of Stages (e.g., 1_Execute, 2_Critique, 3_Reflect).

1_Execute (or 1_translate / 1_create_story): Takes the current Playbook (a list of best-practice instructions) and the raw Input (e.g., Chinese poem) to produce an output JSON.

2_Critique: Takes the raw Input, the model's output from Stage 1, and a human-provided Ground Truth (expert translations/stories). It outputs a JSON of strengths and weaknesses.

3_Reflect: Takes the weaknesses and main_critique from Stage 2 and generates new, actionable instructions called learned_patterns.

Curator (ace_util.py): The process method passes the learned_patterns to the internal curator, which adds them to the global Playbook.

Iteration: The next Job in the sequence repeats the process, feeding the now-improved Playbook into its own 1_Execute stage, resulting in a smarter prompt and better output.
