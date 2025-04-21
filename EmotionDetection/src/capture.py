import cv2
import time
import os

class CameraCapture:
    def __init__(self, camera_id=0, output_dir='captured_images'):
        """Initialize camera capture module."""
        self.camera_id = camera_id
        self.output_dir = output_dir
        self.cap = None
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def start_camera(self):
        """Start the camera."""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
        return True
    
    def capture_frame(self):
        """Capture a single frame from the camera."""
        if self.cap is None or not self.cap.isOpened():
            self.start_camera()
        
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Failed to capture frame")
        return frame
    
    def save_frame(self, frame, filename=None):
        """Save the captured frame to disk."""
        if filename is None:
            filename = f"frame_{int(time.time())}.jpg"
        
        file_path = os.path.join(self.output_dir, filename)
        cv2.imwrite(file_path, frame)
        return file_path
    
    def capture_for_emotion(self):
        """Capture frame specifically for emotion detection."""
        frame = self.capture_frame()
        return frame
    
    def display_with_feedback(self, seconds=5):
        """Display camera feed with countdown for user preparation."""
        if self.cap is None:
            self.start_camera()
        
        start_time = time.time()
        while time.time() - start_time < seconds:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Add countdown text
            remaining = int(seconds - (time.time() - start_time))
            cv2.putText(frame, f"Capturing in: {remaining}s", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('Prepare for Emotion Capture', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Capture the final frame for emotion detection
        ret, frame = self.cap.read()
        cv2.destroyAllWindows()
        return frame
    
    def release(self):
        """Release the camera resources."""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()