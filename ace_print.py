import argparse
import json

def print_prompt(file_path, system_only=False, poem_file=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not data:
                print("No data found in the file.")
                return

            last_entry = data[-1]
            current_ace_prompt = last_entry.get('current_ace_prompt', None)
            if not current_ace_prompt:
                print("No current_ace_prompt found in the last entry.")
                return

            lines = current_ace_prompt.split('\n')
            system_prompt = []
            strategies = []
            in_system = False
            in_strategies = False

            for line in lines:
                if line.strip() == "--- SYSTEM PROMPT ---":
                    in_system = True
                    continue
                if line.strip() == "--- PLAYBOOK (for next run) ---":
                    in_system = False
                    in_strategies = True
                    continue  
                if in_system:
                    system_prompt.append(line)
                if in_strategies:
                    strategies.append(line)

            if system_only:
                # print("System Prompt:")
                print('\n'.join(system_prompt))
            else:
                #print("Full Prompt (System + Strategies):")
                print("Important!  Follow all strategies in PLAYBOOK ")
                print(current_ace_prompt)

            if poem_file:
                try:
                    with open(poem_file, 'r', encoding='utf-8') as poem:
                        poem_text = poem.read().strip()
                        print("\nPOEM:")
                        print(poem_text)
                except FileNotFoundError:
                    print(f"\nError: Poem file '{poem_file}' not found.")
                except Exception as e:
                    print(f"\nError reading poem file: {e}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def print_all_playbook_snapshots(file_path, last_only=False):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not data:
                print("No data found in the file.")
                return

            if last_only:
                last_entry = data[-1]
                playbook_snapshot = last_entry.get('playbook_snapshot', {})
                if playbook_snapshot:
                    print("Last Playbook Snapshot:")
                    print(json.dumps(playbook_snapshot, indent=2, ensure_ascii=False))
                else:
                    print("No playbook_snapshot found in the last entry.")
            else:
                for i, entry in enumerate(data, 1):
                    playbook_snapshot = entry.get('playbook_snapshot', {})
                    if playbook_snapshot:
                        print(f"Playbook Snapshot {i}:")
                        print(json.dumps(playbook_snapshot, indent=2, ensure_ascii=False))
                        print("-" * 40)
                    else:
                        print(f"No playbook_snapshot found in entry {i}.")
                        print("-" * 40)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Print playbook_snapshots or prompts from a JSON file.')
    parser.add_argument('-f', '--file', required=True, help='Path to the JSON file')
    parser.add_argument('-l', '--last', action='store_true', help='Print only the last playbook_snapshot')
    parser.add_argument('-s', '--system', action='store_true', help='Print only the system prompt from the last current_ace_prompt')
    parser.add_argument('-p', '--prompt', action='store_true', help='Print the full prompt (system + strategies) from the last current_ace_prompt')
    parser.add_argument('--poem', help='Append the poem text from the specified file (must be used with -s or -p)')
    args = parser.parse_args()

    if args.poem and not (args.system or args.prompt):
        parser.error("--poem must be used with -s or -p")

    if args.system or args.prompt:
        print_prompt(args.file, args.system, args.poem)
    else:
        print_all_playbook_snapshots(args.file, args.last)

if __name__ == "__main__":
    main()

