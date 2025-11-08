import os
import sys
import json
from ace_util import AcePipeline # Assumes 'ace_pipeline.py' is in the same directory

# --- 1. DEFINE YOUR PIPELINE STAGES ---
# (Paste the POETRY_STAGES dictionary from above here)
POETRY_STAGES = {
    # Stage 1: Analyze the styles...
    "1_analyze_styles": {
        "system_prompt": "You are an expert literary critic and translator, specializing in Tang Dynasty poetry and its English reception. Your analysis is precise and insightful. Return ONLY valid JSON.",
        "playbook_section": "extraction",
        "temperature": 0.1,
        "user_prompt_template": """
PLAYBOOK (strategies for analyzing translation):
{playbook}

DATA (JSON of existing translations by experts):
{translations_json}

PROCESS:
Analyze the different translation styles in the provided JSON. For each translator (Hinton, Rexroth, Watson), describe their approach in one or two sentences.
- Are they literal or interpretive?
- What is their tone (e.g., modern, academic, archaic)?
- What key choices do they make in 'Spring Prospect'?

JSON FORMAT:
{{
  "style_analysis": {{
    "hinton": "A brief analysis of Hinton's style...",
    "rexroth": "A brief analysis of Rexroth's style...",
    "watson": "A brief analysis of Watson's style..."
  }}
}}
"""
    },
    
    # Stage 2: Synthesize principles...
    "2_synthesize_principles": {
        "system_prompt": "You are a master translator of Tang Dynasty poets, creating a style guide for your students. You are synthesizing best practices. Return ONLY valid JSON.",
        "playbook_section": "validation",
        "temperature": 0.2,
        "user_prompt_template": """
PLAYBOOK (strategies for good translation):
{playbook}

DATA (Style analysis from the previous step):
{1_analyze_styles_json}

PROCESS:
Based on the style analysis, synthesize a set of "Best-Practice Principles" for translating Du Fu. These principles should aim to create a translation that is both accurate to the original's tone (grief, separation, duty) and poetically powerful in English.

JSON FORMAT:
{{
  "translation_principles": [
    "Principle 1: e.g., 'Must preserve the 5-character line structure where possible.'",
    "Principle 2: e.g., 'The tone must capture both personal grief and national tragedy.'",
    "Principle 3: e.g., 'Avoid overly modern idioms that break the classical tone.'"
  ]
}}
"""
    },
    
    # Stage 3: Reflect...
    "3_reflect": {
        "system_prompt": "You are a senior editor at a university press, reviewing a new translator's style guide. You are meticulous and aim to improve the guide. Return ONLY valid JSON.",
        "playbook_section": "all",
        "temperature": 0.3,
        "user_prompt_template": """
DATA (Original translations):
{translations_json}

GROUND TRUTH (Considered the source of truth for this task):
{ground_truth_json}

MY 'FINAL IDENTIFICATION' (The principles I just generated):
{2_synthesize_principles_json}

PROCESS:
Compare the 'translation_principles' I just generated against the 'GROUND TRUTH' (the actual expert translations).
- Are my principles too vague?
- Do they fail to account for a specific choice one of the experts made (e.g., Watson's handling of 'tears')?
- What new 'learned_pattern' (a better, more specific principle) can I add to my playbook to create a *better* style guide next time?

JSON FORMAT:
{{
    "critique": "A brief critique of my generated principles, pointing out one weakness.",
    "learned_patterns": [
        "A new, actionable strategy for analyzing translations (e.g., 'Always check how translators handle parallel structures.')",
        "A refined, more specific translation principle to use in the future."
    ]
}}
"""
    }
}


# --- 2. DEFINE YOUR DATA AND CONSTANTS ---

# This is the 'data' and 'ground_truth' you provided
POEM_DATA = {
  "translations_by_author": {
    "hinton": [
      {
        "title_en": "Spring Prospect",
        "title_cn": "春望",
        "original_chinese": "國破山河在，城春草木深。感時花濺淚，恨別鳥驚心。烽火連三月，家書抵萬金。白頭搔更短，渾欲不勝簪。",
        "translation": "The state is broken, but mountains and rivers remain. Spring comes to the city, grasses and trees grow thick. Moved by the times, flowers splash tears. Grieving separation, birds alarm the heart. Beacon fires have burned for three months now. A letter from home is worth ten thousand pieces of gold. I scratch my white hair, which has grown shorter, until it’s almost too sparse to hold a hatpin."
      },
      {
        "title_en": "Moonlit Night",
        "title_cn": "月夜",
        "original_chinese": "今夜鄜州月，閨中只獨看。遙憐小兒女，未解憶長安。香霧雲鬟濕，清輝玉臂寒。何時倚虛幌，雙照淚痕乾。",
        "translation": "Tonight, the Fuchou moon. In her chamber, she watches all alone. I gaze at my distant children, so small they can’t remember Ch’ang-an. Her fragrant mist-cloud hair is damp, her clear-jade arms cold in moonlight. When will we lean in the empty window, moon bright on us, our tears dried?"
      },
      {
        "title_en": "Gazing at the Sacred Peak",
        "title_cn": "望岳",
        "original_chinese": "岱宗夫如何？齊魯青未了。造化鍾神秀，陰陽割昏曉。盪胸生曾雲，決眥入歸鳥。會當凌絕頂，一覽眾山小。",
        "translation": "For all this, what is a the mountain god like? An unending green of lands north and south: from ethereal beauty Creation distills there, yin and yang split dusk and dawn. Swelling clouds sweep by. Returning birds ruin my eyes vanishing. One day soon, at the summit, the other mountains will be small enough to hold, all in a single glance."
      }
    ],
    "rexroth": [
      # ... (omitted for brevity, but it's the full JSON) ...
      {
        "title_en": "Spring Prospect",
        "title_cn": "春望",
        "original_chinese": "國破山河在，城春草木深。感時花濺淚，恨別鳥驚心。烽火連三月，家書抵萬金。白頭搔更短，渾欲不勝簪。",
        "translation": "The capital is fallen, but the hills and rivers remain. The city in spring is thick with weeds and grass. Grieving for the times, the flowers sprinkle tears. Hating the parting, the birds cry out in alarm. The beacon fires have flamed for three months. A letter from home is worth ten thousand pieces of gold. I scratch my white hair. It has grown so thin. It will no longer hold the pin."
      },
      {
        "title_en": "Moonlit Night",
        "title_cn": "月夜",
        "original_chinese": "今夜鄜州月，閨中只獨看。遙憐小兒女，未解憶長安。香霧雲鬟濕，清輝玉臂寒。何時倚虛幌，雙照淚痕乾。",
        "translation": "The moon shines in Fu-Chou tonight, In her chamber, she watches alone. I pity my distant boy and girl. They don't know why she thinks of Ch'ang-an. Her cloud-like hair is sweet with mist, Her jade arms cold in the clear moonlight. When shall we lean together in the empty window, Together in brightness, our tears dried?"
      },
      {
        "title_en": "Gazing at the Sacred Peak",
        "title_cn": "望岳",
        "original_chinese": "岱宗夫如何？齊魯青未了。造化鍾神秀，陰陽割昏曉。盪胸生曾雲，決眥入歸鳥。會當凌絕頂，一覽眾山小。",
        "translation": "What shall I say of the Great Peak? The eternal green of Ch’i and Lu. Here the Creator has gathered all magic. North and south it divides the dusk and dawn. My breast is filled with clouds. My eyes are filled with flocks of birds. I must claim to the very top. From there I shall see all the other mountains, summed up in a single glance."
      }
    ],
    "watson": [
       {
        "title_en": "Spring Prospect",
        "title_cn": "春望",
        "original_chinese": "國破山河在，城春草木深。感時花濺淚，恨別鳥驚心。烽火連三月，家書抵萬金。白頭搔更短，渾欲不勝簪。",
        "translation": "The nation shattered, mountains and river remain; city in spring, grass and trees burgeoning. Feeling the times, blossoms draw tears; hating separation, birds alarm the heart. Beacon fires three months in succession, a letter from home worth ten thousand in gold. White hairs, fewer for the scratching, soon too few to hold a hairpin up."
      },
      {
        "title_en": "Moonlit Night",
        "title_cn": "月夜",
        "original_chinese": "今夜鄜州月，閨中只獨看。遙憐小兒女，未解憶長安。香霧雲鬟濕，清輝玉臂寒。何時倚虛幌，雙照淚痕乾。",
        "translation": "Tonight in Fuzhou she watches the moon alone, and I think of my small son and daughter far away, too young to understand what's keeping me in Chang'an. Her cloud-soft hair must be damp with fragrant mist, her jade-white arms cold in the clear moonlight. When will we lean together by the empty curtains, the moonlight drying the tear-streaks on our faces?"
      },
      {
        "title_en": "Gazing at the Sacred Peak",
        "title_cn": "望岳",
        "original_chinese": "岱宗夫如何？齊魯青未了。造化鍾神秀，陰陽割昏曉。盪胸生曾雲，決眥入歸鳥。會當凌絕頂，一覽眾山小。",
        "translation": "And what's it like, the great Mount Tai? Through Qi and Lu, one endless green. Here the Creator lavished holy beauty, the northern and southern slopes dividing dusk and dawn. Swelling clouds sweep the breast. Straining eyes catch birds returning. One day I must mount the very summit; with one glance, see all mountains small."
      }
    ]
  }
}


# This is the 'data' packaged as the 'inputs' object
# We must pass the JSON as a string in the prompt
pipeline_inputs = {
    "translations_json": json.dumps(POEM_DATA) 
}

# This is the 'ground_truth'
# The process() method will stringify this for us
pipeline_ground_truth = POEM_DATA


HISTORY_FILE = "poetry_analysis_history.json"


# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    
    # Check for API Key
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set your API key, e.g.:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        sys.exit(1)

    # 1. Initialize the pipeline
    ace = AcePipeline(api_key=API_KEY)
    
    # 2. Load any past history and restore the playbook
    ace.load_history(HISTORY_FILE)

    # 3. Process the translation data
    run_results = ace.process(
        pipeline_id="DuFu_Analysis_Run_1",
        stages=POETRY_STAGES,
        inputs=pipeline_inputs,
        ground_truth=pipeline_ground_truth
    )
    
    # 4. Save progress
    ace.save_history(HISTORY_FILE)


    # --- 4. SHOW RESULTS ---
    
    print("\n" + "="*60)
    print("FINAL 'IDENTIFICATION' (Generated Translation Principles)")
    print("="*60)
    
    # Get the 'final identification' from the last run
    final_identification = run_results.get("2_synthesize_principles_data", {})
    
    if final_identification:
        print(json.dumps(final_identification, indent=2, ensure_ascii=False))
    else:
        print("Error: Could not retrieve final identification data.")
    
    # Show how the playbook grew
    ace.show_playbook_evolution()
