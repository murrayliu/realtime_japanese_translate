import pyaudio
import numpy as np
import wave

# Set up parameters
samplerate = 44100  # Adjust as needed
duration = 10       # Adjust as needed
output_file = 'recorded_audio.wav'

# Set up PyAudio
p = pyaudio.PyAudio()

# Choose the input device (you might need to find the appropriate index for your system)
# You can list available devices using: p.get_device_count() and p.get_device_info_by_index(index)
input_device_index = 1  # Change this to the correct index for your system

# Set up the audio stream
stream = p.open(format=pyaudio.paInt16,
                channels=2,  # Stereo
                rate=samplerate,
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=1024)

# Record audio and save it to a WAV file
frames = []
print("Recording...")
for _ in range(int(samplerate / 1024 * duration)):
    data = stream.read(1024)
    frames.append(data)

print("Finished recording.")

# Close the stream and save the recorded audio to a file
stream.stop_stream()
stream.close()

wf = wave.open(output_file, 'wb')
wf.setnchannels(2)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(samplerate)
wf.writeframes(b''.join(frames))
wf.close()

p.terminate()
