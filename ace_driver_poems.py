import os
import sys
import json
from ace_util import AcePipeline # Assumes 'ace_pipeline.py' is in the same directory

# --- 1. DEFINE YOUR NEW PIPELINE STAGES ---

POETRY_STAGES = {
    # Stage 1: The "Execute" stage. Translate the poem.
    "1_translate": {
        "system_prompt": "You are an expert translator of Tang Dynasty poetry (Du Fu, Li Bai). Your goal is to create translations that are poetically powerful in English while remaining faithful to the original's tone, imagery, and meaning.",
        "playbook_section": "translation",
        "temperature": 0.2, # A little creativity, but not too much
        "user_prompt_template": """
{playbook}

PROCESS:
Translate the following Chinese poem into English. 

DATA (Original Chinese):
{original_chinese}

JSON FORMAT:
{{
  "title_cn": "{title_cn}",
  "title_en": "Your translated title",
  "gemini_translation": "Your full translated poem as a single string."
}}
"""
    },
    
    # Stage 2: The "Critique" stage. Compare Gemini to Experts.
    "2_critique": {
        "system_prompt": "You are a literary critic comparing translations. You are precise, fair, and identify specific strengths and weaknesses. Return ONLY valid JSON.",
        "playbook_section": "critique",
        "temperature": 0.1,
        "user_prompt_template": """
DATA (Original Chinese):
{original_chinese}

GROUND TRUTH (Expert Human Translations):
{ground_truth_json}

MY TRANSLATION (from Stage 1):
{1_translate_json}

PROCESS:
Critically compare my 'MY TRANSLATION' against the 'GROUND TRUTH' expert translations.
- What specific phrases or lines did the experts handle better?
- What specific phrases or lines did I handle well or in an interesting new way?
- What is the key weakness of 'MY TRANSLATION' (e.g., missed tone, wrong word choice, awkward phrasing)?

JSON FORMAT:
{{
  "strengths": [
    "A specific strength of my translation (e.g., 'Good handling of line 1').",
    "..."
  ],
  "weaknesses": [
    "A specific weakness (e.g., 'Missed the meaning of "渾欲不勝簪" in the final line.')",
    "..."
  ],
  "main_critique": "A one-sentence summary of the main difference between my translation and the experts."
}}
"""
    },
    
    # Stage 3: The "Reflect" stage. Generate new prompt instructions.
    "3_reflect": {
        "system_prompt": "You are a senior editor and prompt engineer. Your goal is to write new, actionable instructions to improve a translator's future work. Return ONLY valid JSON.",
        "playbook_section": "all",
        "temperature": 0.3,
        "user_prompt_template": """
DATA (Critique from Stage 2):
{2_critique_json}

GROUND TRUTH (Expert Human Translations):
{ground_truth_json}

PROCESS:
Based *only* on the 'weaknesses' and 'main_critique' from the critique, generate one or two new, specific, actionable instructions for the translator (the 'learned_patterns').
- These instructions will be added to the playbook for the *next* translation.
- They should be short and direct.
- Example: "Instruction: 'Pay close attention to the final couplet, as it often holds the poem's core emotion.'"
- Example: "Instruction: 'When you see the character "淚" (tears), consider if it's literal (crying) or metaphorical (grieving), like the experts do.'"

JSON FORMAT:
{{
    "learned_patterns": [
        "A new, actionable instruction for the translation prompt.",
        "Another new, actionable instruction."
    ]
}}
"""
    }
}


# --- 2. DEFINE YOUR DATA AND CONSTANTS ---

# Here is your data, structured as a list of "jobs"
# Each job has the input data and the ground truth
POEM_JOBS = [
    {
        "id": "DuFu_Spring_Prospect",
        "inputs": {
            "title_cn": "春望",
            "original_chinese": "國破山河在，城春草木深。感時花濺淚，恨別鳥驚心。烽火連三月，家書抵萬金。白頭搔更短，渾欲不勝簪。"
        },
        "ground_truth": {
            "hinton": "The state is broken, but mountains and rivers remain. Spring comes to the city, grasses and trees grow thick. Moved by the times, flowers splash tears. Grieving separation, birds alarm the heart. Beacon fires have burned for three months now. A letter from home is worth ten thousand pieces of gold. I scratch my white hair, which has grown shorter, until it’s almost too sparse to hold a hatpin.",
            "rexroth": "The capital is fallen, but the hills and rivers remain. The city in spring is thick with weeds and grass. Grieving for the times, the flowers sprinkle tears. Hating the parting, the birds cry out in alarm. The beacon fires have flamed for three months. A letter from home is worth ten thousand pieces of gold. I scratch my white hair. It has grown so thin. It will no longer hold the pin.",
            "watson": "The nation shattered, mountains and river remain; city in spring, grass and trees burgeoning. Feeling the times, blossoms draw tears; hating separation, birds alarm the heart. Beacon fires three months in succession, a letter from home worth ten thousand in gold. White hairs, fewer for the scratching, soon too few to hold a hairpin up."
        }
    },
    {
        "id": "DuFu_Moonlit_Night",
        "inputs": {
            "title_cn": "月夜",
            "original_chinese": "今夜鄜州月，閨中只獨看。遙憐小兒女，未解憶長安。香霧雲鬟濕，清輝玉臂寒。何時倚虛幌，雙照淚痕乾。"
        },
        "ground_truth": {
            "hinton": "Tonight, the Fuchou moon. In her chamber, she watches all alone. I gaze at my distant children, so small they can’t remember Ch’ang-an. Her fragrant mist-cloud hair is damp, her clear-jade arms cold in moonlight. When will we lean in the empty window, moon bright on us, our tears dried?",
            "rexroth": "The moon shines in Fu-Chou tonight, In her chamber, she watches alone. I pity my distant boy and girl. They don't know why she thinks of Ch'ang-an. Her cloud-like hair is sweet with mist, Her jade arms cold in the clear moonlight. When shall we lean together in the empty window, Together in brightness, our tears dried?",
            "watson": "Tonight in Fuzhou she watches the moon alone, and I think of my small son and daughter far away, too young to understand what's keeping me in Chang'an. Her cloud-soft hair must be damp with fragrant mist, her jade-white arms cold in the clear moonlight. When will we lean together by the empty curtains, the moonlight drying the tear-streaks on our faces?"
        }
    },
    {
        "id": "DuFu_Gazing_at_the_Sacred_Peak",
        "inputs": {
            "title_cn": "望岳",
            "original_chinese": "岱宗夫如何？齊魯青未了。造化鍾神秀，陰陽割昏曉。盪胸生曾雲，決眥入歸鳥。會當凌絕頂，一覽眾山小。"
        },
        "ground_truth": {
            "hinton": "For all this, what is a the mountain god like? An unending green of lands north and south: from ethereal beauty Creation distills there, yin and yang split dusk and dawn. Swelling clouds sweep by. Returning birds ruin my eyes vanishing. One day soon, at the summit, the other mountains will be small enough to hold, all in a single glance.",
            "rexroth": "What shall I say of the Great Peak? The eternal green of Ch’i and Lu. Here the Creator has gathered all magic. North and south it divides the dusk and dawn. My breast is filled with clouds. My eyes are filled with flocks of birds. I must claim to the very top. From there I shall see all the other mountains, summed up in a single glance.",
            "watson": "And what's it like, the great Mount Tai? Through Qi and Lu, one endless green. Here the Creator lavished holy beauty, the northern and southern slopes dividing dusk and dawn. Swelling clouds sweep the breast. Straining eyes catch birds returning. One day I must mount the very summit; with one glance, see all mountains small."
        }
    }
]


HISTORY_FILE = "poetry_translator_history.json"


# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        sys.exit(1)

    # 1. Initialize the pipeline
    ace = AcePipeline(api_key=API_KEY)
    
    # 2. Load any past history and restore the playbook
    ace.load_history(HISTORY_FILE)

    # 3. Loop through each poem and process it
    # The playbook will get smarter with each loop
    all_final_results = []
    
    for job in POEM_JOBS:
        run_results = ace.process(
            pipeline_id=job["id"],
            stages=POETRY_STAGES,
            inputs=job["inputs"],
            ground_truth=job["ground_truth"]
        )
        
        # Save the "final identification" (Gemini's translation)
        final_translation_data = run_results.get("1_translate_data", {})
        all_final_results.append(final_translation_data)
        
        # Save progress after each poem
        ace.save_history(HISTORY_FILE)


    # --- 4. SHOW RESULTS ---
    
    print("\n" + "="*60)
    print("FINAL GEMINI TRANSLATIONS (After learning)")
    print("="*60)
    
    for result in all_final_results:
        print("\n----------------------------------")
        print(f"Title: {result.get('title_en')} ({result.get('title_cn')})")
        print("----------------------------------")
        print(result.get('gemini_translation', 'Translation failed.'))
    
    # Show how the playbook grew
    ace.show_playbook_evolution()

