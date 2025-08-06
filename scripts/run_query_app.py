# FILE: scripts/run_query_app.py
# ACTION: Replace the entire content of your existing scripts/run_query_app.py with this.

# --- FIX: Add project root to Python path ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --- END FIX ---

import argparse
import yaml
from dotenv import load_dotenv
from src.query_engine import create_query_engine

def main():
    # --- FIX: Load environment variables from .env file ---
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run a query app for a specific domain.")
    parser.add_argument("--domain", required=True, help="The domain to query (e.g., ai_education).")
    args = parser.parse_args()

    # 1. Load config
    config_path = f"configs/{args.domain}_config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 2. Create query engine
    query_engine = create_query_engine(
        config['vector_collection_name'],
        config.get('system_prompt') # Use .get() for safety
    )
    
    print(f"--- Query App for '{args.domain}' is ready. Type 'exit' to quit. ---")

    # 3. Interactive loop
    while True:
        query = input("Ask your question: ")
        if query.lower() == 'exit':
            break
        response = query_engine.query(query)
        print("\nResponse:")
        print(response)
        print("---")

if __name__ == "__main__":
    main()
