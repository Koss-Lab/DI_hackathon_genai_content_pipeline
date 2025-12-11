# cli.py
import sys
from src.pipeline import ContentPipeline

pipeline = ContentPipeline(use_api=True)

# ---------------------------------------------------------
# Option 1 - Default prompts pipeline
# ---------------------------------------------------------
def run_default_pipeline():
    results = pipeline.run()
    print("\n--- RESULTS ---")
    print(results)
    print("----------------\n")

# ---------------------------------------------------------
# Option 2 - Custom prompt
# ---------------------------------------------------------
def run_custom_prompt():
    prompt = input("\nEnter your prompt: ")
    results = pipeline.process_single(prompt)   # FIXED
    print("\n--- RESULTS ---")
    print(results)
    print("----------------\n")

# ---------------------------------------------------------
# Option 3 - Batch CSV
# ---------------------------------------------------------
def run_batch_csv():
    csv_path = "data/prompts.csv"
    print(f"[CLI] Using default CSV file: {csv_path}")
    results = pipeline.run_batch_csv(csv_path)  # FIXED
    print("\n--- RESULTS ---")
    print(results)
    print("----------------\n")

# ---------------------------------------------------------
# Option 4 - View last results
# ---------------------------------------------------------
def view_last_results():
    results = pipeline.get_last_results()
    print("\n--- LAST RESULTS ---")
    print(results)
    print("----------------\n")

# ---------------------------------------------------------
# Menu loop
# ---------------------------------------------------------
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
            sys.exit(0)
        else:
            print("Invalid input. Try again.\n")


if __name__ == "__main__":
    main()
