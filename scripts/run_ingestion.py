# FILE: scripts/run_ingestion.py
# ACTION: Replace the entire content of your existing scripts/run_ingestion.py with this.

# --- FIX: Add project root to Python path ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --- END FIX ---

import argparse
import yaml
from dotenv import load_dotenv
from src.data_ingestion import load_from_directory, load_from_urls
from src.indexing import build_index

def main():
    # --- FIX: Load environment variables from .env file ---
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run data ingestion for a specific domain.")
    parser.add_argument("--domain", required=True, help="The domain to process (e.g., ai_education).")
    args = parser.parse_args()

    # 1. Load config
    config_path = f"configs/{args.domain}_config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 2. Load data from all sources
    local_docs = load_from_directory(config['local_data_path'])
    web_docs = load_from_urls(config['urls_to_scrape'])
    all_documents = local_docs + web_docs
    
    print(f"Total documents loaded: {len(all_documents)}")

    # 3. Build and persist the index
    if all_documents:
        build_index(config['vector_collection_name'], all_documents)
        print(f"--- Ingestion for domain '{args.domain}' complete! ---")
    else:
        print("No documents found to index. Exiting.")


if __name__ == "__main__":
    main()
