import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import requests
import zipfile
import io

class EmotionDetector:
    def __init__(self, model_path= "E:\Codes\EmotionDetection\models\emotion_model.h5"):

        self.model = None
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
        
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load the emotion detection model."""
        try:
            self.model = load_model(model_path)
            print("Emotion detection model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def predict_emotion(self, preprocessed_face):
        """Predict emotion from preprocessed face image."""
        if self.model is None:
            raise Exception("Model not loaded")
        
        if preprocessed_face is None:
            return {"error": "No face detected"}
        
        # Make prediction
        predictions = self.model.predict(preprocessed_face)
        emotion_idx = np.argmax(predictions[0])
        emotion = self.emotion_labels[emotion_idx]
        confidence = float(predictions[0][emotion_idx])
        
        # Return prediction with confidence score
        result = {
            "emotion": emotion,
            "confidence": confidence,
            "all_emotions": {label: float(score) for label, score in zip(self.emotion_labels, predictions[0])}
        }
        
        return result
    
    def map_emotion_to_mood(self, emotion_result):
        """Map detected emotion to a simplified mood for music generation."""
        if "error" in emotion_result:
            return "neutral"  # Default mood if no face detected
        
        # Map emotions to simplified moods for music generation
        emotion_to_mood = {
            "happy": "happy",
            "surprise": "energetic",
            "neutral": "calm",
            "sad": "melancholic",
            "fear": "tense",
            "angry": "intense",
            "disgust": "dark"
        }
        
        return emotion_to_mood[emotion_result["emotion"]]
    
    def get_model(self): 
        return self.model