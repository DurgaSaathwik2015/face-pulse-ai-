import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from config import BANDPASS_LOW_HZ, BANDPASS_HIGH_HZ

def prepare_signal(values, timestamps):
    x = np.asarray(values, dtype=float)
    t = np.asarray(timestamps, dtype=float)
    if len(x) != len(t) or len(x) < 30:
        return np.array([]), 0.0
    good = np.isfinite(x) & np.isfinite(t)
    x, t = x[good], t[good]
    order = np.argsort(t)
    x, t = x[order], t[order]
    unique = np.r_[True, np.diff(t) > 1e-5]
    x, t = x[unique], t[unique]
    if len(t) < 30 or t[-1] <= t[0]:
        return np.array([]), 0.0
    fs = 1.0 / np.median(np.diff(t))
    if fs < 10:
        return np.array([]), fs
    target_fs = min(fs, 30.0)
    grid = np.arange(t[0], t[-1], 1.0 / target_fs)
    if len(grid) < 30:
        return np.array([]), target_fs
    x = interp1d(t, x, kind="linear", fill_value="extrapolate")(grid)
    x = signal.detrend(x, type="linear")
    high = min(BANDPASS_HIGH_HZ, target_fs / 2 - 0.5)
    if high <= BANDPASS_LOW_HZ:
        return np.array([]), target_fs
    sos = signal.butter(3, [BANDPASS_LOW_HZ, high], btype="bandpass", fs=target_fs, output="sos")
    filtered = signal.sosfiltfilt(sos, x)
    return filtered, target_fs
