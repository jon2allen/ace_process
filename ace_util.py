import json
import google.generativeai as genai
from typing import Dict, Any, List
import os
import time

class AcePipeline:
    """
    A general-purpose, self-correcting pipeline that uses an 
    Analyze-Critique-Execute (ACE) loop.
    (Full class code from our previous conversation)
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        print(f"Initializing AcePipeline with model: {model_name}")
        self.model_name = model_name
        self._setup_client(api_key)
        self.playbook = {
            "process_strategies": [],
            "critique_strategies": [],
        }
        self.history = []

    def _setup_client(self, api_key: str):
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            print(f"Error configuring Google AI: {e}")
            raise
        self.generation_config = genai.GenerationConfig(
            response_mime_type="application/json", 
        )

    def _call_llm(self, system_prompt: str, user_prompt: str, temperature: float = 0.1) -> str:
        start_time = time.time()
        try:
            model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_prompt
            )
            config = self.generation_config
            config.temperature = temperature
            print(f"  ... Calling {self.model_name} (Temp: {temperature}) ...")
            response = model.generate_content(
                user_prompt,
                generation_config=config
            )
            call_time = time.time() - start_time
            print(f"  ... LLM call complete ({call_time:.2f}s)")
            return response.text
        except Exception as e:
            print(f"  ⚠ LLM Call Error: {e}")
            return "{}"

    def _parse_json(self, json_string: str, stage_name: str) -> Dict:
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"  ⚠ [{stage_name}] Critical: Failed to parse JSON from LLM.")
            print(f"  Raw response: {json_string}")
            raise e

    def curator(self, reflection: Dict) -> Dict:
        print("\n[CURATOR] Updating playbook...")
        for pattern in reflection.get("learned_patterns", []):
            # We will just use one category for simplicity
            if pattern not in self.playbook["process_strategies"]:
                self.playbook["process_strategies"].append(pattern)
                print(f"  ✓ Added prompt strategy: {pattern[:80]}...")
        
        # Keep playbook manageable
        self.playbook["process_strategies"] = self.playbook["process_strategies"][-10:]
        print(f"\nPlaybook now contains:")
        print(f"  - {len(self.playbook['process_strategies'])}  prompt strategies")
        return self.playbook

    def _format_playbook(self, section: str = "all") -> str:
        playbook = self.playbook
        if not any(playbook.values()):
            return "No strategies learned yet. This is your first attempt."

        formatted = ""
        print("section : ", section )
        if section in ["all", section ] and playbook.get("process_strategies"):
            formatted += "PROCESS STRATEGIES (learned from previous critiques):\n"
            for i, s in enumerate(playbook["process_strategies"], 1):
                formatted += f"{i}. {s}\n"
        
        return formatted if formatted else "No strategies learned yet for this section."

    def process(
        self, 
        pipeline_id: str,
        stages: Dict[str, Dict], 
        inputs: Dict[str, Any], 
        ground_truth: Dict = None
    ) -> Dict:
        print(f"\n{'='*60}")
        print(f"PROCESSING: {pipeline_id} (using {len(stages)} stages)")
        print(f"{'='*60}")
        
        run_context = inputs.copy()
        run_context["pipeline_id"] = pipeline_id
        
        for stage_name in sorted(stages.keys()):
            stage_def = stages[stage_name]
            print(f"\n[STAGE: {stage_name}]")

            # Store the system prompt for this stage in the run's history
            run_context[f"{stage_name}_system_prompt"] = stage_def.get("system_prompt", "No system prompt defined")

            playbook_str = self._format_playbook(
                section=stage_def.get("playbook_section", "all")
            )
            run_context["playbook"] = playbook_str
            
            if ground_truth:
                run_context["ground_truth_json"] = json.dumps(ground_truth, indent=2, ensure_ascii=False)
            else:
                run_context["ground_truth_json"] = "None provided."

            try:
                user_prompt = stage_def["user_prompt_template"].format_map(run_context)
            except KeyError as e:
                print(f"  ⚠ Missing key '{e}' for prompt template. Skipping stage.")
                continue

            llm_response_str = self._call_llm(
                system_prompt=stage_def["system_prompt"],
                user_prompt=user_prompt,
                temperature=stage_def.get("temperature", 0.1)
            )
            
            try:
                result_json = self._parse_json(llm_response_str, stage_name)
                run_context[f"{stage_name}_json"] = llm_response_str
                run_context[f"{stage_name}_data"] = result_json
                print(f"  ✓ Stage complete.")
            except Exception as e:
                print(f"  ✗ Stage failed on JSON parse: {e}")
                return run_context

        last_stage_name = sorted(stages.keys())[-1]
        last_stage_data = run_context.get(f"{last_stage_name}_data", {})
        
        if "learned_patterns" in last_stage_data:
            print("\n[STAGE: CURATION]")
            self.playbook = self.curator(last_stage_data)
        else:
            print(f"\n[INFO] No 'learned_patterns' found in final stage ('{last_stage_name}').")
            print("       Playbook not updated. This is normal for inference runs.")
            
        run_context["playbook_snapshot"] = self.playbook.copy()

        # --- NEW CODE ---
        # At the end of the pipeline, build the prompt for the *next* run
        
        # 1. Get the system prompt from the *first* stage (e.g., "1_translate")
        #    We assume the first stage is the main "execute" prompt that evolves.
        first_stage_name = sorted(stages.keys())[0]
        first_stage_system_prompt = stages[first_stage_name].get("system_prompt", "No first stage system prompt")
        
        # 2. Format the *newly updated* playbook
        next_playbook_str = self._format_playbook(
            section=stages[first_stage_name].get("playbook_section", "all")
        )

        # 3. Combine them to create the prompt that will be used for the *next* run
        current_ace_prompt = (
            f"--- SYSTEM PROMPT ---\n{first_stage_system_prompt}\n\n" +
            f"--- PLAYBOOK (for next run) ---\n{next_playbook_str}"
        )
        
        # 4. Save this to the history
        run_context["current_ace_prompt"] = current_ace_prompt
        # --- END NEW CODE ---
        
        self.history.append(run_context)

        return run_context

    def show_playbook_evolution(self):
        print(f"\n{'='*60}")
        print("PLAYBOOK EVOLUTION (Refined Prompt Instructions)")
        print(f"{'='*60}")

        if not self.history:
            print("No history recorded yet.")
            return

        for i, history_item in enumerate(self.history, 1):
            pb = history_item["playbook_snapshot"]
            print(f"\nAfter Run: {history_item['pipeline_id']}:")
            print(f"  Strategies: {len(pb.get('process_strategies', []))}")

        print(f"\n{'='*60}\nFINAL PLAYBOOK (These are your new prompt instructions)\n{'='*60}")
        print(self._format_playbook(section="all"))

    def save_history(self, filepath: str):
        print(f"\n[IO] Saving history with {len(self.history)} runs to {filepath}...")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            print(f"  ✓ History saved successfully.")
        except IOError as e:
            print(f"  ⚠ Error saving history: {e}")
        except TypeError as e:
            print(f"  ⚠ Error serializing history (non-serializable data): {e}")

    def load_history(self, filepath: str):
        print(f"\n[IO] Loading history from {filepath}...")
        if not os.path.exists(filepath):
            print(f"  ✓ No history file found at {filepath}. Starting fresh.")
            return
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
            if not self.history:
                print("  ✓ History file was empty. Starting fresh.")
                return
            latest_playbook = self.history[-1].get("playbook_snapshot")
            if latest_playbook:
                self.playbook = latest_playbook
                print(f"  ✓ History loaded {len(self.history)} runs.")
                print("  ✓ Playbook restored from last run.")
            else:
                print("  ⚠ History loaded, but no playbook snapshot found in last run.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"  ⚠ Error loading history: {e}. Starting fresh.")
            self.history = []





