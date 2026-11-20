import numpy as np

def assess_quality(timestamps, brightness, face_flags, fs):
    reasons = []
    t = np.asarray(timestamps, dtype=float)
    b = np.asarray(brightness, dtype=float)
    f = np.asarray(face_flags, dtype=bool)
    level = "Good"
    if len(t) < 30:
        reasons.append("Too few valid face samples.")
        level = "Poor"
    if fs < 10:
        reasons.append("Sampling rate is too low.")
        level = "Poor"
    if len(f) and np.mean(f) < 0.85:
        reasons.append("Face tracking was lost frequently.")
        level = "Poor" if np.mean(f) < 0.6 else "Moderate"
    if len(b) > 2 and np.std(b) > 18:
        reasons.append("Lighting changed substantially during recording.")
        level = "Poor" if np.std(b) > 35 else ("Moderate" if level == "Good" else level)
    if len(t) > 2:
        intervals = np.diff(t)
        med = np.median(intervals)
        if med <= 0 or np.max(np.abs(intervals - med)) > max(0.12, 2.5 * med):
            reasons.append("Frame timestamps are irregular.")
            level = "Moderate" if level == "Good" else level
    return {"level": level, "reasons": reasons}
