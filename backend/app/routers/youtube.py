import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import librosa
import tensorflow as tf
from app.utils.youtube_to_wav import download_youtube_as_wav
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the APIRouter
router = APIRouter()

# Load the pre-trained model (ensure the path is correct)
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'my_model.h5')

# Log the model loading
logger.debug(f"Loading model from {model_path}")
model = tf.keras.models.load_model(model_path)
logger.debug("Model loaded successfully.")

# Define the GTZAN genres
genres = [
    "blues", "classical", "country", "disco", 
    "hiphop", "jazz", "metal", "pop", "reggae", "rock"
]

class YouTubeRequest(BaseModel):
    url: str

def extract_mel_spectrogram(file_path: str, start_time: float, duration: float = 4.0):
    try:
        logger.debug(f"Extracting Mel spectrogram from {file_path}, starting at {start_time}s for {duration}s.")
        # Load the audio file from the start time
        y, sr = librosa.load(file_path, sr=22050, offset=start_time, duration=duration)
        # Convert the audio into a Mel spectrogram
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        # Convert to log scale (dB)
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
        
        # Add the batch dimension and channel dimension (i.e., shape becomes [1, 150, 150, 1])
        log_mel_spectrogram = np.expand_dims(log_mel_spectrogram, axis=-1)  # Add channel dimension
        log_mel_spectrogram = np.expand_dims(log_mel_spectrogram, axis=0)   # Add batch dimension
        
        # Resize the spectrogram to match the model's expected input size
        log_mel_spectrogram_resized = tf.image.resize(log_mel_spectrogram, [150, 150])
        
        logger.debug("Mel spectrogram extraction and resizing successful.")
        return log_mel_spectrogram_resized
    except Exception as e:
        logger.error(f"Error during Mel spectrogram extraction: {str(e)}")
        raise



@router.post("/predict-youtube")
def predict_genre_from_youtube(request: YouTubeRequest):
    try:
        logger.info(f"Received YouTube URL: {request.url}")

        # Download the YouTube audio as a WAV file
        output_path = "./wav_files"
        os.makedirs(output_path, exist_ok=True)
        logger.info(f"Downloading audio from {request.url} to {output_path}.")
        wav_path = download_youtube_as_wav(request.url, output_path)

        # Log the downloaded WAV file path
        logger.info(f"Downloaded WAV file saved at {wav_path}")

        # Extract audio duration
        y, sr = librosa.load(wav_path, sr=22050)
        audio_duration = librosa.get_duration(y=y, sr=sr)
        logger.info(f"Audio duration: {audio_duration} seconds")

        # Initialize a list to store predictions
        predictions = []

        # Iterate over the audio in 4-second chunks with 2-second overlap
        chunk_duration = 4.0  # 4 seconds
        overlap = 2.0  # 2 seconds overlap
        start_time = 0.0
        
        while start_time + chunk_duration <= audio_duration:
            # Extract mel spectrogram for the current chunk
            mel_spectrogram = extract_mel_spectrogram(wav_path, start_time, chunk_duration)

            # Predict the genre for the current chunk
            logger.debug(f"Predicting genre for chunk starting at {start_time}s.")
            prediction = model.predict(mel_spectrogram)
            predicted_class = np.argmax(prediction)
            predictions.append(predicted_class)
            logger.debug(f"Predicted class: {predicted_class} for chunk starting at {start_time}s.")

            # Move the start time by 2 seconds (overlap)
            start_time += overlap

        # Determine the majority vote for the final genre
        predicted_class_majority = np.bincount(predictions).argmax()
        predicted_genre = genres[predicted_class_majority]
        logger.info(f"Final predicted genre: {predicted_genre}")

        return {"predicted_genre": predicted_genre}

    except Exception as e:
        logger.exception("An error occurred while processing the request.")
        raise HTTPException(status_code=500, detail="Internal Server Error. Check server logs.")
