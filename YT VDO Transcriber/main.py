import os
from pytube import YouTube
from moviepy.editor import AudioFileClip
import speech_recognition as sr

def clean_youtube_url(url):
    if '&' in url:
        url = url.split('&')[0]
    return url

def download_audio_from_youtube(youtube_url, output_path="audio.wav"):
    try:
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        audio_file_path = video.download(filename="audio")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

    try:
        audio_clip = AudioFileClip(audio_file_path)
        audio_clip.write_audiofile(output_path, codec='pcm_s16le')
        os.remove(audio_file_path)
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None
    
    return output_path

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)
            return transcription
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def save_transcription(transcription, output_file):
    with open(output_file, "w") as file:
        file.write(transcription)

def main(youtube_url, output_transcription_file):
    youtube_url = clean_youtube_url(youtube_url)
    audio_path = "audio.wav"
    downloaded_audio_path = download_audio_from_youtube(youtube_url, audio_path)
    if downloaded_audio_path:
        transcription = transcribe_audio(downloaded_audio_path)
        save_transcription(transcription, output_transcription_file)
        print(f"Transcription saved to {output_transcription_file}")
    else:
        print("Failed to download or process the audio.")

if __name__ == "__main__":
    youtube_url = input("Enter YouTube video URL: ")
    output_transcription_file = "transcription.txt"
    main(youtube_url, output_transcription_file)
