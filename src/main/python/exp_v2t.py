# === version 1 ===
# import assemblyai as aai
# aai.settings.api_key = "6ea73535df834863afd8815e58563f13"
# transcriber = aai.Transcriber()
# transcript = transcriber.transcribe("record/rec_v1.wav")
# print(transcript.text)


# === version 2 ===
import speech_recognition as sr
r = sr.Recognizer()
WAV = sr.AudioFile('record/rec_v1.wav')
with WAV as source:
    print(source.CHUNK)
    print(source.FRAME_COUNT)
    print(source.SAMPLE_RATE)
    print(source.DURATION)
    print(source.stream)
    audio = r.record(source)

print(r.recognize_google(audio, show_all=False))