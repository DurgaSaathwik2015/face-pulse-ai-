import numpy as np
from src.rppg import green_channel_signal, pos_signal
from src.heart_rate import estimate_bpm
from evaluation.metrics import calculate_metrics

def test_green_signal_centered():
    y = green_channel_signal([1, 2, 3])
    assert abs(y.mean()) < 1e-9

def test_pos_output_length():
    t = np.arange(900) / 30
    rgb = np.column_stack([100 + np.sin(2*np.pi*1.2*t),
                           110 + 2*np.sin(2*np.pi*1.2*t),
                           90 + np.sin(2*np.pi*1.2*t)])
    assert len(pos_signal(rgb, 30)) == len(t)

def test_metrics():
    m = calculate_metrics([60, 70], [62, 68])
    assert m["MAE"] == 2
