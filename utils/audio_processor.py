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
        "quiet":True,  # if this is false then the dowloading process  is visible on terminal
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from {url}...")
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav").replace(".mp4",".wav")
    return filename


def convert_to_wav(input_path:str)->str:
    """convert any audio/video file to WAV format using pydub"""
    output_path=os.path.splitext(input_path)[0]+ "_converted.wav"
    audio=AudioSegment.from_file(input_path)
    audio=audio.set_channels(1).set_frame_rate(16000) # set_channels Convert audio to mono and set_frame_rate 16000 Hz (16 kHz)
    audio.export(output_path,format="wav")
    return output_path  




# this is use for makeing  video chuck of  10min 
def chunk_audio(wav_pata :str,chunk_minutes:int=10)->list:
    audio=AudioSegment.from_wav(wav_pata) #This loads a WAV audio file into Python using the pydub library.
    chunk_ms=chunk_minutes*60*1000
    chunks=[]

   # enumerate mean we will make index and data differently 
   # len will be in millisecond 
    for i,start in enumerate(range(0,len(audio),chunk_ms)):
        chunk=audio[start:start+chunk_ms] # this is slicing syntax
        chunk_path=f"{wav_pata}_chunk_{i}.wav"
        chunk.export(chunk_path,format="wav")
        chunks.append(chunk_path)
    return chunks

def process_input(source: str)->list:
    if source.startswith("http://")  or source.startswith("https://"):
        print("Detected Youtube URL. Dowloading audio...")
        wav_path=download_youtube_audio(source)
    else:
        print("Detected local file.Converting to Wav..")
        wav_path=convert_to_wav(source)
    
    print("Chuncking audio...")
    chunks=chunk_audio(wav_path)
    print(f"Audio ready -- {len(chunks)} chunk(s) created.")
    return chunks


