# FILE: scripts/run_evaluation.py
# ACTION: Create this new file in your scripts/ directory.

# --- Add project root to Python path ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# --- END FIX ---

import argparse
import yaml
import json
from dotenv import load_dotenv
from src.query_engine import create_query_engine
from src.evaluation import run_evaluation

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Run evaluation for a specific RAG domain.")
    parser.add_argument("--domain", required=True, help="The domain to evaluate (e.g., ai_education).")
    args = parser.parse_args()

    # 1. Load Domain Config
    config_path = f"configs/{args.domain}_config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 2. Load Evaluation Set
    eval_set_path = f"evaluation_sets/{args.domain}_eval.json"
    with open(eval_set_path, 'r') as f:
        eval_data = json.load(f)
    
    eval_questions = [item['question'] for item in eval_data]
    ground_truths = [item['ground_truth'] for item in eval_data]

    # 3. Create Query Engine
    query_engine = create_query_engine(
        config['vector_collection_name'],
        config.get('system_prompt')
    )
    
    # 4. Run Evaluation
    print(f"--- Starting Evaluation for domain: {args.domain} ---")
    run_evaluation(query_engine, eval_questions, ground_truths)
    print(f"--- Evaluation for domain: {args.domain} complete! ---")


if __name__ == "__main__":
    main()
