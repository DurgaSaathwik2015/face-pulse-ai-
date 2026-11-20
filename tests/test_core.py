import numpy as np
from src.rppg import green_channel_signal, pos_signal
from src.heart_rate import estimate_bpm
from src.signal_quality import get_quality_guidance
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

def test_quality_guidance_is_actionable_and_deduplicated():
    guidance = get_quality_guidance([
        "Face tracking was lost frequently.",
        "Lighting changed substantially during recording.",
        "Face tracking was lost frequently.",
        "Unexpected quality issue.",
    ])
    assert guidance == [
        "Center your face, keep still, and improve front-facing lighting.",
        "Use steady, diffuse lighting and avoid changing lights during the recording.",
        "Repeat the measurement with steady lighting and minimal movement.",
    ]
