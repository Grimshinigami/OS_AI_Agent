import pvporcupine
import pyaudio
import numpy as np
from dotenv import load_dotenv
import os
# Create a Porcupine instance with the keyword "ok google"
load_dotenv()

porcupine = pvporcupine.create(
  access_key=os.environ["ACCESS_KEY"],
  keyword_paths=[os.environ["KEYWORD_1"], os.environ['KEYWORD_2']]
)

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for the keyword 'Hey Vice'...")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = np.frombuffer(pcm, dtype=np.int16)

        # Detect the keyword
        keyword_index = porcupine.process(pcm)
        if keyword_index == 0:
            print("Keyword Hey Vice detected!")
        elif keyword_index == 1:
            print("Exit keyword detected now exiting...")
            break
finally:
    audio_stream.close()
    porcupine.delete()
