import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompts import system_prompt
from google.generativeai.types import content_types, generation_types
from collections.abc import Iterable
from PIL import ImageGrab
import mouse
from pynput.keyboard import Key,Controller
import pvporcupine
import numpy as np
import edge_tts
import asyncio
import wave
import librosa
import soundfile as sf
import pyaudio
import speech_recognition as sr
from groq import Groq
import time
import pyttsx3
import uiautomation as automation
import json
import pygame
import re

load_dotenv()

avail_fns = [
    'look_at_screen_and_respond', 
    'use_keyboard',
    'list_elements_of_current_window',
    'find_and_click_element',
    'launch_app'
]

text_to_voice = ""

response_txt = ""

applist = {
    0:"Chrome.exe",
    1:"Spotify.exe",
    2:"Explorer.exe",
    3:"calc.exe",
    4:"taskmgr.exe",
    5:"notepad.exe"
}

def conditions(response:generation_types.GenerateContentResponse):
    # print(response.candidates[0].content.parts)
    fc = ""
    global response_txt
    global text_to_voice
    # for i in response.candidates[0].content.parts:
    #     print(i.function_response)
    midresponse = response.candidates[0].content.parts
    for i in midresponse:
        if i.function_call.name in avail_fns:
            fc = i.function_call
            print(fc)
        else:
            response_txt = i
            # print(fc)
    # if len(response.candidates[0].content.parts)>1:
    #     fc = response.candidates[0].content.parts[1].function_call
    #     print(fc)

    if response_txt.text!="" or re.search('[a-zA-Z]',response_txt.text):
        print(response_txt.text)
        text_to_voice=""

    if fc!="":
        if fc.name == 'look_at_screen_and_respond':
            look_at_screen_and_respond()
        elif fc.name == 'click_on_screen':
            print("Inside click on screen")
            print("X-coordinate: ",fc.args['x'])
            print("Y-coordinate: ",fc.args['y'])
            print("Press Enter?: ",fc.args['twotimes'])
            click_on_screen(fc.args['x'],fc.args['y'],fc.args['twotimes'])
        elif fc.name == 'use_keyboard':
            print("Inside use_keyboard function")
            print("Key value is: ", fc.args['keywords'])
            use_keyboard(fc.args['keywords'], fc.args['press_enter'])
        elif fc.name == 'list_elements_of_current_window':
            print("Inside list_elements_of_current_window function")
            list_elements_of_current_window()
        elif fc.name == 'find_and_click_element':
            print("Inside find_and_click_element function")
            find_and_click_element(fc.args['target_name'])
        elif fc.name == 'launch_app':
            print("Inside launch_app function")
            launch_app(fc.args['launch_index'])
    # else:
    #     print(response.candidates[0].content.parts[0].text)

def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
    """Create a tool config with the specified function calling mode."""
    return content_types.to_tool_config(
        {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
    )

def look_at_screen_and_respond():
    '''
    Gets a screenshot of the current window that will be send to the gemini model for analysis along with a prompt.

    Args:
        None
    
    Returns:
        None
    '''

    screenshot = ImageGrab.grab()

    screenshot.save("screenshot.png")

    screenshot.close()

    myfile = genai.upload_file('screenshot.png')

    os.remove('screenshot.png')

    response = chat.send_message([myfile, "Here is a screenshot of the current window"], tool_config=tool_config)

    conditions(response)
    # print(response.text)

def click_on_screen(x:int, y:int, twotimes:bool):
    '''
    Moves the mouse pointer to the desired x and y coordinates and then simulates left click of mouse.
    Also lets the user decide whether the click should be single or double.

    Args:
        x: The X-Coordinate of the screen to which pointer must be moved.
        y: The Y-Coordinate of the screen to which pointer must be moved.
        twotimes: Decides whether to perform a single click or double click
    Returns:
        None
    '''
    
    mouse.move(x,y)
    mouse.click('left')
    if twotimes:
        mouse.click('left')
    
    response = chat.send_message("Click on the required coordinates has been done",tool_config=tool_config)

    conditions(response)

def use_keyboard(keywords: str, press_enter:bool=False):
    '''
    Types a given value in whatever input field is currently selected. It does this action by simulating keystrokes.

    Args:
        keywords: The value or text string which needs to be typed in the input field
        press_enter: Bool value to check if enter should be pressed or not false by default
    Returns:
        None
    '''

    keyboard = Controller()
    content = keywords.split('\\n')
    for i in content:
        keyboard.type(i.strip())
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.1)
    
    if press_enter:
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

    response = chat.send_message("Provided message has been printed",tool_config=tool_config)

    conditions(response)


def set_continue_loop(value_to_set:bool):
    '''
    Sets the continue loop variable to the provided value
    continue_loop decides whether to continue the model loop or not to perform more action or get more information

    Args:
        value_to_set: A bool value which can be True or False, continue_loop is set to this value.

    Returns:
        None
    '''
    global continue_loop
    continue_loop = value_to_set

async def get_wave():
    global response_txt
    communicate = edge_tts.Communicate(response_txt.text, voice="en-US-ChristopherNeural", rate="+20%", pitch="-8Hz")
    # await communicate.stream()
    await communicate.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove('output.mp3')

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
        # print(transcription.text.strip())
        text_to_voice = transcription.text.strip()
        os.remove("user_input_voice.wav")

def listen_to_user():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening now...")
        audio_data = recognizer.listen(source)
        with open("user_input_voice.wav", "wb") as f:
            f.write(audio_data.get_wav_data())
        print("Done Listening...")

def get_voice():
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Text you want to convert to speech
    global response_txt

    # Set properties before playing (optional)
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)

    # Pass the text to the engine
    engine.say(response_txt.text)

    # Run the speech engine
    engine.runAndWait()

def list_ui_elements_to_dict(control, depth=0):

    element_dict = {
        "name": control.Name,
        "control_type": control.ControlTypeName,
        "children": []
    }
    
    # Recursively process children
    for child in control.GetChildren():
        element_dict["children"].append(list_ui_elements_to_dict(child, depth + 4))
    
    return element_dict

def list_elements_of_current_window():
    '''
    A function that lists all the available clickable elements in the current active window 
    and sends the data in a json string format to the model.

    Args:
        None
    
    Returns:
        None
    '''

    time.sleep(5)

    # while True:

    active_window = automation.GetForegroundControl()

    # Create a dictionary for the active window
    ui_elements_dict = {
        "name": active_window.Name,
        "control_type": active_window.ControlTypeName,
        "children": []
    }

    # Populate the dictionary with UI elements

    ui_elements_dict["children"] = [list_ui_elements_to_dict(child) for child in active_window.GetChildren()]

    json_object = json.dumps(ui_elements_dict, indent=2)

    print("JSON Object is: \n",json_object)

    response = chat.send_message(["Here are all the elements in a json string: ",json_object],tool_config=tool_config)

    conditions(response)

def see_through_elements(control, target_name=None, target_control_type=None):
    # if target_name and control.Name == target_name:
    if target_name and target_name in control.Name:
        print(f"Found: {control.Name}, Control Type: {control.ControlTypeName} -> Clicking it.")
        control.Click()
        return True
    if target_control_type and control.ControlTypeName == target_control_type:
        print(f"Found: {control.Name}, Control Type: {control.ControlTypeName} -> Clicking it.")
        control.Click()
        return True

    # Recursively search for the element
    for child in control.GetChildren():
        if see_through_elements(child, target_name, target_control_type):
            return True
    return False

def find_and_click_element(target_name:str):
    '''
    A function which takes the element name available on screen, this is the name field of any object in the 
    json string object provided through the list_elements_of_current_window function and then clicks it using the 
    mouse pointer.

    Args:
        target_name: It is the same as the value of name field of an object in the json string provided through list_elements_of_current_window 
        which lists the elements in the current active window.
    Returns:
        None
    '''


    # Get the current active window
    active_window = automation.GetForegroundControl()

    # Print the active window's details
    print(f"Active Window: {active_window.Name}, Control Type: {active_window.ControlTypeName}")

    # Example: Try to find and click a button by its name or control type
    result = see_through_elements(active_window, target_name)  # Find by name
    # OR
    # find_and_click_element(active_window, target_control_type="Button")  # Find by control type

    if result:
        print("Element Found and Clicked Successfully")
        response = chat.send_message("Clicked on the element given in target_name",tool_config=tool_config)
        conditions(response)
    else:
        print("Couldn't Find Element")
        response = chat.send_message("Could not click on the element given in target_name",tool_config=tool_config)
        conditions(response)
    
    

def launch_app(launch_index:int):
    '''
    A function which launches an app provided the launch_index, the launch_index is a key in the object 
    applist which :
    applist = {
        0:"Chrome.exe",
        1:"Spotify.exe",
        2:"Explorer.exe",
        3:"calc.exe",
        4:"taskmgr.exe",
        5:"notepad.exe"
    }

    When provided with the key, the function launches the corresponding app.

    Args:
        launch_index: Key in the applist object corresponding to the app that needs to be launched.
    
    Returns:
        None
    '''


    try:
        os.startfile(applist[launch_index])
    # os.startfile('D:/Softwares/Open HW Monitor/openhardwaremonitor-v0.9.6/OpenHardwareMonitor/OpenHardwareMonitor.exe')
        print("App opened successfully")
        response = chat.send_message("Launched the app with the provided launch_index",tool_config=tool_config)
        conditions(response)
    except:
        print("Couldn't open this app")
        response = chat.send_message("Couldn't launch the app or wrong launch_index",tool_config=tool_config)
        conditions(response)

genai.configure(api_key=os.environ["API_KEY"])

porcupine = pvporcupine.create(
  access_key=os.environ["ACCESS_KEY"],
  keyword_paths=[os.environ["KEYWORD_1"], os.environ['KEYWORD_2']]
)

available_fn = [
    look_at_screen_and_respond,
    use_keyboard,
    list_elements_of_current_window,
    find_and_click_element,
    launch_app
]

model = genai.GenerativeModel(
    # "models/gemini-1.5-pro",
    "models/gemini-1.5-flash",
    system_instruction=system_prompt,
    tools=available_fn
    # tools=[{'function_declarations': [get_response_time_declaration]}]
)

# response = model.generate_content("Write a poem about friendship")
# print(response.text)
chat = model.start_chat()


tool_config = tool_config_from_mode("auto")
# # tool_config = tool_config_from_mode("any", avail_fns)


# pa = pyaudio.PyAudio()
# audio_stream = pa.open(
#     rate=porcupine.sample_rate,
#     channels=1,
#     format=pyaudio.paInt16,
#     input=True,
#     frames_per_buffer=porcupine.frame_length
# )

# print("Listening for the keyword 'Hey Vice'...")

# try:
#     while True:
#         pcm = audio_stream.read(porcupine.frame_length)
#         pcm = np.frombuffer(pcm, dtype=np.int16)

#         # Detect the keyword
#         keyword_index = porcupine.process(pcm)
#         if keyword_index == 0:
#             print("Keyword Hey Vice detected!")
#             play_audio('start_prompt.wav')
#             listen_to_user()
#             get_voice_to_text()
#             response = chat.send_message(text_to_voice, tool_config=tool_config)
#             conditions(response)
#             asyncio.run(get_wave())
#             # convert()
#             # play_audio('newoutput.wav')
#             # get_voice()
#             print("Listening for the keyword 'Hey Vice'...")
#         elif keyword_index == 1:
#             print("Exit keyword detected now exiting...")
#             break
# finally:
#     audio_stream.close()
#     porcupine.delete()

# continue_loop = True

# while continue_loop:
# inp = input("Enter your task: ")
# response = chat.send_message(inp, tool_config=tool_config)



# print(response.candidates[0].content.parts[0].text)
# count = 0

# while continue_loop:
#     count+=1
#     print(count)
# conditions(response)
while True:
    inp = input('Enter you task/Send more message?')
    if inp=="!EXIT":
        break

    if inp=="":
        inp = input('Enter you task/Send more message?')

    response = chat.send_message(inp, tool_config=tool_config)
    conditions(response)
#     print(response.candidates[0].content.parts)


# print("Response is: ",response)
# print("Response.candidates are: ",response.candidates)
# print("Response.candidates[0].content are: ",response.candidates[0].content)
# print("Response.candidates[0].content.parts: ",response.candidates[0].content.parts)
# print("Response.candidates[0].content.parts[0].function_call: ",response.candidates[0].content.parts[0].function_call)