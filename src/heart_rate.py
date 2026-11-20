import numpy as np
from scipy.signal import welch

def estimate_bpm(filtered, fs, bpm_range=(45, 180)):
    result = {"valid": False, "bpm": None, "reasons": []}
    x = np.asarray(filtered, dtype=float)
    if fs <= 0 or len(x) < int(fs * 10):
        result["reasons"].append("Not enough usable filtered signal.")
        return result
    freqs, power = welch(x, fs=fs, nperseg=min(len(x), int(fs * 20)))
    low, high = bpm_range[0] / 60.0, bpm_range[1] / 60.0
    mask = (freqs >= low) & (freqs <= high)
    if not np.any(mask):
        result["reasons"].append("No frequencies inside the selected BPM range.")
        return result
    band_power = power[mask]
    idx = np.argmax(band_power)
    peak_power = float(band_power[idx])
    median_power = float(np.median(band_power) + 1e-12)
    peak_hz = float(freqs[mask][idx])
    prominence = peak_power / median_power
    if prominence < 2.0:
        result["reasons"].append("Pulse-frequency peak is weak or ambiguous.")
        return result
    result.update(valid=True, bpm=peak_hz * 60.0, peak_ratio=prominence)
    return result
