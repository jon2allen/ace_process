import os
import sys
import json
from ace_util import AcePipeline # 

def load_config_from_json(file_path):
    """
    Loads STAGES and JOBS from a specified JSON config file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        stages = data.get("STAGES")
        jobs = data.get("JOBS")
        
        if not stages:
            print(f"Error: 'STAGES' key not found in {file_path}")
            return None, None
            
        if not jobs:
            print(f"Error: 'JOBS' key not found in {file_path}")
            return None, None
            
        print(f"Successfully loaded {len(stages)} stages and {len(jobs)} jobs from {file_path}")
        return stages, jobs
        
    except FileNotFoundError:
        print(f"Error: Config file not found at {file_path}")
        return None, None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred loading config: {e}")
        return None, None

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    
    # --- 1. Get Config File from Command Line ---
    if len(sys.argv) != 2:
        print("Usage: python run_pipeline.py <path_to_config.json>")
        sys.exit(1)
        
    CONFIG_FILE = sys.argv[1]
    
    # --- 2. Load Stages and Jobs from Config ---
    PIPELINE_STAGES, PIPELINE_JOBS = load_config_from_json(CONFIG_FILE)
    
    if not PIPELINE_STAGES or not PIPELINE_JOBS:
        sys.exit(1)
        
    # --- 3. Define Constants ---
    # Create a history file name based on the config file name
    HISTORY_FILE = CONFIG_FILE.replace(".json", "") + "_history.json"
    
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        sys.exit(1)

    # --- 4. Initialize and Run Pipeline ---
    
    # 1. Initialize the pipeline
    ace = AcePipeline(api_key=API_KEY)
    
    # 2. Load any past history and restore the playbook
    ace.load_history(HISTORY_FILE)

    # 3. Dynamically find the name of the *first* stage (e.g., "1_translate" or "1_create_story")
    # This assumes stages are named in order, e.g., "1_...", "2_..."
    try:
        first_stage_name = sorted(PIPELINE_STAGES.keys())[0]
        first_stage_data_key = f"{first_stage_name}_data"
        print(f"Identified first stage: '{first_stage_name}'. Will save results from '{first_stage_data_key}'.")
    except IndexError:
        print("Error: 'STAGES' dictionary is empty. Cannot determine first stage.")
        sys.exit(1)

    # 4. Loop through each job and process it
    all_final_results = []
    
    for job in PIPELINE_JOBS:
        print(f"\n--- Processing Job: {job['id']} ---")
        run_results = ace.process(
            pipeline_id=job["id"],
            stages=PIPELINE_STAGES,
            inputs=job.get("inputs", {}),
            ground_truth=job.get("ground_truth", {})
        )
        
        # Save the "final" data (output from the first stage)
        final_data = run_results.get(first_stage_data_key, {})
        all_final_results.append(final_data)
        
        # Save progress after each job
        ace.save_history(HISTORY_FILE)
        print(f"--- Completed Job: {job['id']} ---")


    # --- 5. SHOW RESULTS ---
    
    print("\n" + "="*60)
    print(f"FINAL RESULTS (from stage: {first_stage_name})")
    print("="*60)
    
    for result in all_final_results:
        print("\n----------------------------------")
        # This generically prints the resulting JSON from the first stage
        print(json.dumps(result, indent=4, ensure_ascii=False))
        
    # Show how the playbook grew
    ace.show_playbook_evolution()
