# FacePulse AI — Version 1

Experimental contactless heart-rate estimation from facial video using remote photoplethysmography (rPPG).

## Requirements
- Python 3.10 or 3.11 (recommended)
- Working webcam
- Good, steady front-facing light

## Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## How to use
1. Allow camera access in the browser.
2. Sit facing the camera in steady light; avoid talking or moving.
3. Select 45 seconds and start measurement.
4. Review the estimated BPM, quality status and filtered waveform.
5. Repeat and compare with a reference device measured at the same time.

## Validation CSV
Create a CSV with columns:
`reference_bpm,estimated_bpm`
Use `evaluation.metrics.calculate_metrics` or `evaluation.validation.evaluate_csv`.

## Important limitations
This is a student research prototype, not a medical device. rPPG is sensitive to motion, lighting, frame rate, camera processing, skin reflectance and ROI tracking. A plausible BPM does not establish accuracy. Validate against a suitable reference device using repeated simultaneous measurements. The quality thresholds in this MVP are heuristic and must be calibrated and documented for a formal study.

## Privacy
The application processes frames in memory and does not intentionally save video or upload it. Streamlit runs locally when launched on your computer. CSV export contains RGB samples, not video.

## Troubleshooting
- Close other apps using the webcam.
- Ensure camera permission is allowed.
- Use Python 3.10/3.11 for compatibility with the pinned MediaPipe build.
- Increase room lighting and keep your face still.
- Follow the on-screen quality tips when a measurement reports issues.
- If the app reports poor quality, repeat the measurement rather than trusting a weak estimate.
