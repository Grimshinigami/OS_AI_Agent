import edge_tts
import asyncio
import wave
import librosa
import soundfile as sf
import pyaudio
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
import os
import pyttsx3
import pygame

load_dotenv()

text_to_voice = '''Hey how are you?'''

async def get_wave():
    global text_to_voice
    communicate = edge_tts.Communicate(text_to_voice, voice="en-US-ChristopherNeural", rate="+15%", pitch="-8Hz")
    # await communicate.stream()
    await communicate.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def get_voice():
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Text you want to convert to speech
    global text_to_voice

    # Set properties before playing (optional)
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Pass the text to the engine
    engine.say(text_to_voice)

    # Run the speech engine
    engine.runAndWait()

def convert():
    x,_ = librosa.load('./output.wav', sr=16000)
    sf.write('newoutput.wav', x, 16000)

def play_audio(file_path):

    # Open the wav file
    wf = wave.open(file_path, 'rb')

    # Create a PyAudio object
    p = pyaudio.PyAudio()

    # Open a stream with the correct format based on the file
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read the audio data in chunks
    chunk_size = 1024
    data = wf.readframes(chunk_size)

    # Play the sound by writing audio data to the stream
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio session
    p.terminate()

def get_voice_to_text():
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    filename = os.path.dirname(__file__) + "/user_input_voice.wav"

    with open(filename, "rb") as file:
    # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()), # Required audio file
            model="distil-whisper-large-v3-en", # Required model to use for transcription
            prompt="Transcribe",  # Optional
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        # Print the transcription text
        global text_to_voice
        print(transcription.text.strip())
        text_to_voice = transcription.text.strip()

def listen_to_user():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening now...")
        audio_data = recognizer.listen(source)
        with open("user_input_voice.wav", "wb") as f:
            f.write(audio_data.get_wav_data())
        print("Done Listening...")
# Run the async function
# asyncio.run(get_wave())
# # # get_wave()
# # # asyncio.run(play_audio_stream())
# # time.sleep(1)
# convert()
# get_voice_to_text()
# convert()
# play_audio('start_prompt.wav')
# listen_to_user()
# get_voice_to_text()
# # One more function will come that send this data to google api
asyncio.run(get_wave())
# convert()
# play_audio('newoutput.wav')

# get_voice()


