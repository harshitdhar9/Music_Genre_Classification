import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def download_youtube_as_wav(url: str, output_path: str) -> str:
    temp_output = "temp_audio.%(ext)s"

    ydl_opts = {
        'format': 'bestaudio/best',  
        'outtmpl': temp_output, 
        'quiet': True, 
        'noplaylist': True,  
    }

    try:

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        downloaded_file = next((f for f in os.listdir() if f.startswith('temp_audio')), None)
        if not downloaded_file:
            raise Exception("Failed to download the audio file")

        wav_file = os.path.join(output_path, "output.wav")

        audio = AudioSegment.from_file(downloaded_file)
        audio.export(wav_file, format="wav")

        os.remove(downloaded_file)

        return wav_file

    except Exception as e:
        print(f"Error in download_youtube_as_wav: {str(e)}")
        return None
