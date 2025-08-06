# FILE: src/evaluation.py
# ACTION: Replace the entire content of your existing src/evaluation.py with this.

import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

def create_evaluation_dataset(query_engine, eval_questions, ground_truths):
    """Generates responses and context for the evaluation set."""
    print("Generating responses for evaluation questions...")
    data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": ground_truths
    }
    for question in eval_questions:
        response = query_engine.query(question)
        data["question"].append(question)
        data["answer"].append(str(response))
        # Extracting source nodes and formatting them for RAGAS
        contexts = [node.get_content() for node in response.source_nodes]
        data["contexts"].append(contexts)
    
    # Convert dictionary to a Hugging Face Dataset object
    return Dataset.from_dict(data)

def run_evaluation(query_engine, eval_questions, ground_truths):
    """Runs the RAGAS evaluation and prints the results."""
    print("Creating evaluation dataset...")
    ragas_dataset = create_evaluation_dataset(query_engine, eval_questions, ground_truths)
    
    print("Initializing RAGAS evaluation...")
    # List of metrics we want to calculate
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]
    
    # Run the evaluation
    result = evaluate(
        dataset=ragas_dataset,
        metrics=metrics,
    )
    
    print("Evaluation complete.")
    # Convert results to a readable format and print
    df = result.to_pandas()
    print("--- RAG Evaluation Results ---")
    print(df.to_string())
    return df
