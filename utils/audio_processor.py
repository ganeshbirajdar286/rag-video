import yt_dlp    #downloads YouTube media
from pydub import  AudioSegment  #audio processing library
import os   #file/folder handling
 
DOWNLOAD_DIR='downloads'

os.makedirs(DOWNLOAD_DIR,exist_ok=True) #exist_ok=True prevents errors if folder already exists

def download_youtube_audio(url :str)->str:
    output_path=os.path.join(DOWNLOAD_DIR,"%(title)s.%(ext)s")
    ydl_opts ={
        "format":"bestaudia/best",  # Downloads highest quality audio only.
        "outtmpl": output_path,
        "postprocessors":[
            {
                "key":"FFmpegExtractAudio",
                "preferredcodec":"wav",
                "preferredquality":"192"
            }
        ], #Uses FFmpeg
#Converts downloaded file to WAV
#Audio quality target: 192kbps
        #"quiet":True,  # if this is false then the dowloading process  is visible on terminal
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav").replace(".mp4",".wav")
    return filename

data =download_youtube_audio("https://youtu.be/sLykke8q2ls?si=-Whq5hniE-A2oM0H")


def convert_to_wav(input_path:str)->str:
    """convert any audio/video file to WAV format using pydub"""
    output_path=os.path.splitext(input_path)[0]+ "_converted.wav"
    print(input_path)
    audio=AudioSegment.from_file(input_path)
    audio=audio.set_channels(1).set_frame_rate(16000) # set_channels Convert audio to mono and set_frame_rate 16000 Hz (16 kHz)
    audio.export(output_path,format="wav")
    return output_path  

print(convert_to_wav(data))