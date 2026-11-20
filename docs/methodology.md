# FacePulse AI V1 methodology

1. Capture webcam frames and timestamps.
2. Track one face using MediaPipe Face Mesh.
3. Form approximate forehead and cheek polygons from facial landmarks.
4. Compute mean RGB values in each valid polygon and average region means.
5. Run either a demeaned green-channel baseline or a POS-style projection.
6. Sort and deduplicate timestamps, interpolate to a regular time grid, detrend and bandpass filter.
7. Use Welch power spectral density in the selected 45–180 BPM interval and convert the strongest peak to BPM.
8. Reject weak peaks and recordings that fail basic sampling/tracking/illumination checks.

The ROI polygons and quality thresholds are engineering choices for this prototype, not validated clinical thresholds. Test across lighting, movement, camera devices and participants. Do not interpret output medically.
