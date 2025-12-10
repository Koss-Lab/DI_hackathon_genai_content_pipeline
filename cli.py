# cli.py

from src.pipeline import ContentPipeline
from dotenv import load_dotenv
load_dotenv()

# ----------------------------------------
# Create ONE pipeline instance globally
# ----------------------------------------
pipeline = ContentPipeline()


# ----------------------------------------
# MENU FUNCTIONS
# ----------------------------------------
def run_default_pipeline():
    results = pipeline.run()
    print("\n--- RESULTS ---")
    print(results)
    print("----------------\n")


def run_custom_prompt():
    user_prompt = input("\nEnter your prompt: ").strip()
    result = pipeline.process_single(user_prompt)
    print("\n--- RESULTS ---")
    print(result)
    print("----------------\n")


def run_batch_csv():
    print("[CLI] Using default CSV file: data/prompts.csv")
    results = pipeline.run_batch_csv("data/prompts.csv")
    print("\n--- RESULTS ---")
    print(results)
    print("----------------\n")


def view_last_results():
    results = pipeline.get_last_results(limit=10)
    if not results:
        print("\nNo previous results found.\n")
        return

    print("\n--- LAST RESULTS ---")
    print(results)
    print("----------------\n")


# ----------------------------------------
# MAIN MENU LOOP
# ----------------------------------------
def main():
    while True:
        print("""
==========================================
      DI GenAI Content Pipeline v1.0
==========================================

1) Run pipeline on default prompts
2) Enter a custom prompt
3) Run batch on CSV file
4) View last results
5) Quit
""")

        choice = input("Select an option: ").strip()

        if choice == "1":
            run_default_pipeline()

        elif choice == "2":
            run_custom_prompt()

        elif choice == "3":
            run_batch_csv()

        elif choice == "4":
            view_last_results()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.\n")


# ----------------------------------------
# LAUNCH
# ----------------------------------------
if __name__ == "__main__":
    main()
