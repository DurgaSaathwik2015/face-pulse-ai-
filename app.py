import time
import cv2
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config import DEFAULT_DURATION, MIN_DURATION, MAX_DURATION, MIN_BPM, MAX_BPM
from src.face_detection import FaceTracker
from src.roi_extraction import extract_roi_means, draw_rois
from src.rppg import green_channel_signal, pos_signal
from src.signal_processing import prepare_signal
from src.heart_rate import estimate_bpm
from src.signal_quality import assess_quality

st.set_page_config(page_title="FacePulse AI", page_icon="💓", layout="wide")
st.title("💓 FacePulse AI")
st.caption("Experimental contactless heart-rate estimation from facial video")
st.warning("Research prototype only — not a medical device. Do not use for diagnosis or treatment.")

with st.sidebar:
    st.header("Measurement settings")
    duration = st.slider("Recording duration (seconds)", MIN_DURATION, MAX_DURATION, DEFAULT_DURATION)
    method = st.selectbox("rPPG method", ["POS (recommended to compare)", "Green channel"])
    bpm_range = st.slider("Search range (BPM)", MIN_BPM, MAX_BPM, (MIN_BPM, MAX_BPM))
    st.caption("Use steady, diffuse lighting. Keep your face still and fill the guide area.")

left, right = st.columns([1.4, 1])
preview = left.empty()
status = left.empty()
progress = left.empty()
result_area = right.container()

if "measurement" not in st.session_state:
    st.session_state.measurement = None

if st.button("Start measurement", type="primary", use_container_width=True):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam. Check camera permissions and close other camera apps.")
    else:
        tracker = FaceTracker()
        samples, timestamps, brightness, face_flags = [], [], [], []
        start = time.time()
        frame_count = 0
        while time.time() - start < duration:
            ok, frame = cap.read()
            if not ok:
                status.error("Camera frame could not be read.")
                break
            now = time.time()
            frame_count += 1
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            landmarks = tracker.detect(rgb)
            brightness.append(float(rgb.mean()))
            face_flags.append(landmarks is not None)
            if landmarks is not None:
                roi = extract_roi_means(rgb, landmarks)
                if roi is not None:
                    samples.append(roi)
                    timestamps.append(now)
                annotated = draw_rois(rgb, landmarks)
                preview.image(annotated, channels="RGB", use_container_width=True)
                status.success("Face detected — keep still")
            else:
                preview.image(rgb, channels="RGB", use_container_width=True)
                status.warning("Face not detected — position your face in the frame")
            elapsed = min(now - start, duration)
            progress.progress(elapsed / duration, text=f"Recording: {int(elapsed)} / {duration} seconds")
        cap.release()
        tracker.close()
        if len(samples) >= 30:
            st.session_state.measurement = {
                "samples": samples, "timestamps": timestamps,
                "brightness": brightness, "face_flags": face_flags,
                "method": method, "bpm_range": bpm_range
            }
        else:
            st.error("Not enough valid face samples were captured. Try again with better lighting and positioning.")

data = st.session_state.measurement
if data:
    raw = pd.DataFrame(data["samples"], columns=["R", "G", "B"])
    t = pd.Series(data["timestamps"], dtype=float).to_numpy()
    fs = 1.0 / (pd.Series(t).diff().dropna().median()) if len(t) > 2 else 0
    quality = assess_quality(t, data["brightness"], data["face_flags"], fs)
    if data["method"].startswith("POS"):
        pulse = pos_signal(raw[["R", "G", "B"]].to_numpy(), fs)
    else:
        pulse = green_channel_signal(raw["G"].to_numpy())
    processed, effective_fs = prepare_signal(pulse, t)
    estimate = estimate_bpm(processed, effective_fs, data["bpm_range"])
    quality["reasons"].extend(estimate.get("reasons", []))
    if not estimate["valid"]:
        quality["level"] = "Poor"
    result_area.subheader("Measurement result")
    if estimate["valid"] and quality["level"] != "Poor":
        result_area.metric("Estimated heart rate", f'{estimate["bpm"]:.1f} BPM')
    else:
        result_area.metric("Estimated heart rate", "Unavailable")
        result_area.info("The signal did not pass the quality checks. No BPM is displayed.")
    result_area.write(f"**Signal quality:** {quality['level']}")
    for reason in dict.fromkeys(quality["reasons"]):
        result_area.write(f"• {reason}")
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(processed, linewidth=0.8)
    ax.set_title("Filtered rPPG signal")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    ax.grid(alpha=0.25)
    st.pyplot(fig)
    st.download_button("Download RGB samples (CSV)", raw.to_csv(index=False), "facepulse_rgb_samples.csv", "text/csv")
    st.caption("Estimates are sensitive to lighting, motion, camera frame rate, skin reflectance and device hardware.")
else:
    result_area.subheader("Ready to measure")
    result_area.write("Start a measurement to capture a short facial video and analyse its pulse-related colour variation.")

st.divider()
st.caption("Privacy: frames are processed locally in this app session and are not saved as video or uploaded by this project.")
