# from django.shortcuts import render
# from django.http import HttpResponse
# from django.conf import settings
# import wave
# import pyaudio
from transformers import pipeline
# import matplotlib.pyplot as plt

# def record_audio(request):
#     if request.method == 'POST':
#         # Configuration for audio recording
#         FORMAT = pyaudio.paInt16
#         CHANNELS = 1
#         RATE = 44100
#         CHUNK = 3200
#         RECORD_SECONDS = 20  # Adjust as needed

#         # Create a PyAudio object
#         p = pyaudio.PyAudio()

#         # Open stream for recording
#         stream = p.open(format=FORMAT,
#                         channels=CHANNELS,
#                         rate=RATE,
#                         input=True,
#                         frames_per_buffer=CHUNK)

#         print("* Recording audio...")

#         frames = []

#         # Record audio for the specified duration
#         for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#             data = stream.read(CHUNK)
#             frames.append(data)
#         # while True:
#         #     data = stream.read(CHUNK)
#         #     frames.append(data)
#         #     if request.POST.get('stop_recording') == 'true':
#         #         break
            
#         print("* Finished recording")

#         # Stop the stream and close PyAudio
#         stream.stop_stream()
#         stream.close()
#         p.terminate()

#         # Save the recorded audio to a file
#         wf = wave.open('audio.wav', 'wb')
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(p.get_sample_size(FORMAT))
#         wf.setframerate(RATE)
#         wf.writeframes(b''.join(frames))
#         wf.close()

#         # Initialize the pipeline for speech recognition
#         speech_recognizer = pipeline("automatic-speech-recognition", model="openai/whisper-small")

#         # Transcribe the audio
#         transcription = speech_recognizer('audio.wav')
#         print(transcription)
#         return HttpResponse(transcription['text'])

#     return render(request, 'record_audio.html')

# #########################################################################

import pyaudio
import wave
import threading
from django.shortcuts import render
from django.http import HttpResponse
speech_recognizer = pipeline("automatic-speech-recognition", model="openai/whisper-small")

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 20
is_recording = False
frames = []
p = pyaudio.PyAudio()
stream = None

def start_recording(request):
    global is_recording, frames, stream
    if not is_recording:
        frames = []
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer=CHUNK)
        print("* Recording Audio ...")
        is_recording = True

        def record_audio():
            global is_recording, frames
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
                if not is_recording:
                    break
            print("* Finished recording")
            stream.stop_stream()
            stream.close()
            p.terminate()

            wf = wave.open('audio.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
           


        
        thread = threading.Thread(target=record_audio)
        thread.start()
        return render(request,'record_audio.html',{'message':"Recording hudei xa hai"})
    else:
        return HttpResponse('Recording is already in progress.')
    
def stop_recording(request):
    global is_recording
    if is_recording:
        is_recording = False
        return render(request,'record_audio.html',{'message':"Record vaisako sathy"})
    else:
        return HttpResponse('No recording is currently in progress.')
      

def record_audio(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'start':
            print("ya aaipugyo")
            return start_recording(request)
        elif request.POST.get('action') == 'stop':
            stop_recording(request)
    # Transcribe the audio
            transcription = speech_recognizer('audio.wav')
            print(transcription['text'])
            return render(request,'record_audio.html',{'transcription':transcription['text']})
    return render(request, 'record_audio.html')

# def record_audio(request):
#     if request.method == 'POST':
#         # Access 'action' parameter sent in the query string
#         action = request.POST.get('action')
#         print(action)
#         if action == 'start':
#             # Handle start recording action
#             return HttpResponse('Recording started.')
#         elif action == 'stop':
#             # Handle stop recording action
#             return HttpResponse('Recording stopped.')
#     return render(request, 'record_audio.html')