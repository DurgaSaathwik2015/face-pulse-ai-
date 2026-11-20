import pandas as pd
from evaluation.metrics import calculate_metrics

def evaluate_csv(path):
    df = pd.read_csv(path)
    required = {"reference_bpm", "estimated_bpm"}
    if not required.issubset(df.columns):
        raise ValueError("CSV must contain reference_bpm and estimated_bpm columns.")
    return calculate_metrics(df.reference_bpm, df.estimated_bpm)
