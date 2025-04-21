import cv2
import numpy as np
from PIL import Image

class EmotionPreprocessor:
    def __init__(self, face_cascade_path='haarcascade_frontalface_default.xml', 
                 target_size=(48, 48), padding_factor=0.2):
        """Initialize the preprocessor with face detection and image resizing settings."""
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + face_cascade_path)
        self.target_size = target_size
        self.padding_factor = padding_factor  # Add padding around detected face
        
    def detect_face(self, image):
        """Detect faces in the image and return the largest face with padding."""
        if image is None:
            return None
            
        # Make a copy to avoid modifying original
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization to improve contrast
        gray = cv2.equalizeHist(gray)
        
        # Detect faces with different parameters
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            # If no face detected, try with more relaxed parameters
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(20, 20)
            )
            
        if len(faces) == 0:
            return None
        
        # Get the largest face
        largest_face_idx = np.argmax([w*h for (x, y, w, h) in faces])
        x, y, w, h = faces[largest_face_idx]
        
        # Add padding around the face
        padding_x = int(w * self.padding_factor)
        padding_y = int(h * self.padding_factor)
        
        # Ensure coordinates don't go out of image bounds
        img_h, img_w = gray.shape
        x_start = max(0, x - padding_x)
        y_start = max(0, y - padding_y)
        x_end = min(img_w, x + w + padding_x)
        y_end = min(img_h, y + h + padding_y)
        
        # Extract face with padding
        face_img = gray[y_start:y_end, x_start:x_end]
        
        # Optional: visualize the detected face for debugging
        # cv2.rectangle(original, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        # cv2.imwrite("detected_face_debug.jpg", original)
        
        return face_img
    
    def preprocess_for_model(self, face_img):
        """Preprocess detected face for the emotion detection model."""
        if face_img is None:
            return None
        
        # Apply additional preprocessing
        # 1. Enhance contrast
        face_img = cv2.equalizeHist(face_img)
        
        # 2. Resize to target size
        face_img = cv2.resize(face_img, self.target_size)
        
        # 3. Normalize pixel values
        face_img = face_img / 255.0
        
        # 4. Expand dimensions for model input (batch, height, width, channels)
        face_img = np.expand_dims(face_img, axis=0)
        face_img = np.expand_dims(face_img, axis=-1)
        
        return face_img
    
    def preprocess_image(self, image):
        """Complete preprocessing pipeline for an image."""
        face = self.detect_face(image)
        if face is None:
            # If no face detected, try with the full image as fallback
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face = cv2.resize(gray, self.target_size)
            return self.preprocess_for_model(face)
        return self.preprocess_for_model(face)
        
    def visualize_preprocessing(self, image, save_path="preprocessing_debug.jpg"):
        """Debug function to visualize what the model sees after preprocessing."""
        face = self.detect_face(image)
        if face is None:
            print("No face detected")
            return
            
        # Original detected face
        orig_face = face.copy()
        
        # After histogram equalization
        equalized = cv2.equalizeHist(face)
        
        # After resizing
        resized = cv2.resize(equalized, self.target_size)
        
        # Create a debug visualization
        debug_img = np.hstack([
            cv2.resize(orig_face, (200, 200)),
            cv2.resize(equalized, (200, 200)),
            cv2.resize(resized, (200, 200))
        ])
        
        cv2.imwrite(save_path, debug_img)
        print(f"Saved preprocessing visualization to {save_path}")