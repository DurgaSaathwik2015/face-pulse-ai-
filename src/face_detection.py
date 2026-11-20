import mediapipe as mp

class FaceTracker:
    """MediaPipe Face Mesh wrapper. Returns normalized landmark coordinates."""
    def __init__(self):
        self.mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False, max_num_faces=1, refine_landmarks=False,
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )

    def detect(self, rgb_frame):
        result = self.mesh.process(rgb_frame)
        if not result.multi_face_landmarks:
            return None
        return result.multi_face_landmarks[0].landmark

    def close(self):
        self.mesh.close()
