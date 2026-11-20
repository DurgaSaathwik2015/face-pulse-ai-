import numpy as np

def calculate_metrics(reference, estimated):
    ref, est = np.asarray(reference, float), np.asarray(estimated, float)
    if len(ref) != len(est) or len(ref) == 0:
        raise ValueError("Reference and estimate arrays must have equal non-zero length.")
    err = est - ref
    mae = float(np.mean(np.abs(err)))
    rmse = float(np.sqrt(np.mean(err ** 2)))
    corr = float(np.corrcoef(ref, est)[0, 1]) if len(ref) > 1 and np.std(ref) and np.std(est) else float("nan")
    bias = float(np.mean(err))
    sd = float(np.std(err, ddof=1)) if len(err) > 1 else 0.0
    return {"MAE": mae, "RMSE": rmse, "Pearson correlation": corr,
            "Bland-Altman bias": bias, "BA lower limit": bias - 1.96 * sd,
            "BA upper limit": bias + 1.96 * sd}
