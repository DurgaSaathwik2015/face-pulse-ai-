# Research review — references specified by the project brief

This document records the intended reading list and a conservative implementation interpretation. It does not claim that the papers validate this student application.

## 1. Remote Plethysmographic Imaging Using Ambient Light (2008)
https://pmc.ncbi.nlm.nih.gov/articles/PMC2717852/
Foundational reference identified in the project brief for camera-based pulse-related imaging under ambient illumination. Read the paper's acquisition conditions and limitations before using it to justify performance claims.

## 2. Algorithmic Principles of Remote PPG (2017)
https://doi.org/10.1109/TBME.2016.2609282
The project brief identifies this as a key reference for skin-reflection models and POS-style pulse extraction. The V1 POS implementation is a simplified engineering implementation and should be checked against the paper's exact algorithm before claiming equivalence.

## 3. DeepPhys (2018)
https://arxiv.org/abs/1805.07888
The brief identifies DeepPhys as a deep-learning approach to video-based physiological measurement. It is background for possible future work only; V1 does not train or integrate DeepPhys.

## 4. rPPG-Toolbox (NeurIPS 2023)
https://github.com/ubicomplab/rPPG-Toolbox
The brief identifies this as a research toolbox and benchmark resource. It may inform future dataset-based evaluation. V1 does not currently integrate the toolbox.

## V1 design decisions
- Green-channel mean intensity is a baseline.
- POS-style projection is included as a second signal extraction path.
- Welch PSD is used to identify a dominant frequency.
- Quality checks are conservative prototype heuristics, not clinical thresholds.
- Performance must be measured against simultaneous reference readings using repeated trials and documented conditions.

## Limitations to investigate
Motion, changing illumination, camera auto-exposure/white balance, frame-rate variation, ROI drift, skin reflectance, short recording duration and device-specific processing can degrade estimates. Correlation alone does not establish agreement. Report MAE, RMSE, Bland–Altman bias/limits and the study conditions; do not claim clinical accuracy.
