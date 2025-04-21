import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np
import librosa
import tensorflow as tf
from app.utils.youtube_to_wav import download_youtube_as_wav
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'model_transfer.h5')

logger.debug(f"Loading model from {model_path}")
model = tf.keras.models.load_model(model_path)
logger.debug("Model loaded successfully.")

genres = [
    "blues", "classical", "country", "disco", 
    "hiphop", "jazz", "metal", "pop", "reggae", "rock"
]

SAMPLE_RATE = 22050
DURATION = 4  
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION
IMG_SIZE = (224, 224) 

class YouTubeRequest(BaseModel):
    url: str

def extract_mel_spectrogram(file_path: str, start_time: float, duration: float = DURATION):
    try:
        logger.debug(f"Extracting Mel spectrogram from {file_path}, starting at {start_time}s for {duration}s.")
        
        y, sr = librosa.load(file_path, sr=SAMPLE_RATE, offset=start_time, duration=duration)
        
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        
        log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)

        log_mel_spectrogram_resized = tf.image.resize(np.expand_dims(log_mel_spectrogram, axis=-1), [IMG_SIZE[0], IMG_SIZE[1]])
        
        mel_rgb = np.repeat(log_mel_spectrogram_resized, 3, axis=-1)
        
        mel_rgb = mel_rgb / np.max(np.abs(mel_rgb))
        
        logger.debug("Mel spectrogram extraction and resizing successful.")
        return np.expand_dims(mel_rgb, axis=0)  
    except Exception as e:
        logger.error(f"Error during Mel spectrogram extraction: {str(e)}")
        raise

@router.post("/predict-youtube")
def predict_genre_from_youtube(request: YouTubeRequest):
    try:
        logger.info(f"Received YouTube URL: {request.url}")

        output_path = "./wav_files"
        os.makedirs(output_path, exist_ok=True)
        logger.info(f"Downloading audio from {request.url} to {output_path}.")
        wav_path = download_youtube_as_wav(request.url, output_path)

        logger.info(f"Downloaded WAV file saved at {wav_path}")

        y, sr = librosa.load(wav_path, sr=SAMPLE_RATE)
        audio_duration = librosa.get_duration(y=y, sr=sr)
        logger.info(f"Audio duration: {audio_duration} seconds")

        predictions = []

        start_time = 0.0
        
        while start_time + DURATION <= audio_duration:
            mel_spectrogram = extract_mel_spectrogram(wav_path, start_time)

            logger.debug(f"Predicting genre for chunk starting at {start_time}s.")
            prediction = model.predict(mel_spectrogram)
            predicted_class = np.argmax(prediction)
            predictions.append(predicted_class)
            logger.debug(f"Predicted class: {predicted_class} for chunk starting at {start_time}s.")

            start_time += DURATION

        predicted_class_majority = np.bincount(predictions).argmax()
        predicted_genre = genres[predicted_class_majority]
        logger.info(f"Final predicted genre: {predicted_genre}")

        return {"predicted_genre": predicted_genre}

    except Exception as e:
        logger.exception("An error occurred while processing the request.")
        raise HTTPException(status_code=500, detail="Internal Server Error. Check server logs.")
