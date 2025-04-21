import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def download_youtube_as_wav(url: str, output_path: str) -> str:
    temp_output = "temp_audio.%(ext)s"

    # yt-dlp options to download audio
    ydl_opts = {
        'format': 'bestaudio/best',  # Best audio quality
        'outtmpl': temp_output,  # Template for saving the file
        'quiet': True,  # Suppress unnecessary logs
        'noplaylist': True,  # Avoid downloading entire playlist
    }

    try:
        # Download the audio using yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Get the downloaded file extension and name
        downloaded_file = next((f for f in os.listdir() if f.startswith('temp_audio')), None)
        if not downloaded_file:
            raise Exception("Failed to download the audio file")

        # Define path for the converted WAV file
        wav_file = os.path.join(output_path, "output.wav")

        # Convert the audio to WAV using pydub
        audio = AudioSegment.from_file(downloaded_file)
        audio.export(wav_file, format="wav")

        # Clean up the temporary file
        os.remove(downloaded_file)

        # Return the path to the WAV file
        return wav_file

    except Exception as e:
        print(f"Error in download_youtube_as_wav: {str(e)}")
        return None
