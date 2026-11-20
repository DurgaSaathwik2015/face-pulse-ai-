import numpy as np

def green_channel_signal(green):
    """Baseline: demeaned green-channel intensity."""
    x = np.asarray(green, dtype=float)
    return x - np.mean(x)

def pos_signal(rgb, fs, window_seconds=1.6):
    """
    Plane-Orthogonal-to-Skin (POS) style extraction.
    Input columns are mean R,G,B values per frame.
    """
    x = np.asarray(rgb, dtype=float)
    if x.ndim != 2 or x.shape[1] != 3 or len(x) < 10 or fs <= 0:
        return np.array([])
    win = max(8, int(window_seconds * fs))
    output = np.zeros(len(x), dtype=float)
    weight = np.zeros(len(x), dtype=float)
    for start in range(0, len(x), max(1, win // 2)):
        end = min(len(x), start + win)
        block = x[start:end]
        if len(block) < 8:
            continue
        mean = block.mean(axis=0)
        if np.any(np.abs(mean) < 1e-8):
            continue
        normalized = block / mean - 1.0
        # POS projection onto a plane orthogonal to skin tone.
        s1 = normalized[:, 1] - normalized[:, 2]
        s2 = normalized[:, 1] + normalized[:, 2] - 2 * normalized[:, 0]
        alpha = np.std(s1) / (np.std(s2) + 1e-8)
        h = s1 + alpha * s2
        h -= h.mean()
        output[start:end] += h
        weight[start:end] += 1
    valid = weight > 0
    output[valid] /= weight[valid]
    return output
