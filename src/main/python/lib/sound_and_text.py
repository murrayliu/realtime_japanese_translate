import yaml
import wave
import pyaudio
import threading
import numpy as np
from enum import Enum
import assemblyai as aai

TARGET = "立體聲混音"

class Recorder(object):
    def __init__(self, cfg):
        self.chucnk = cfg[CfgEnum.chucnk]
        self.format = pyaudio.paInt16
        self.channels = cfg[CfgEnum.n_channels]
        self.rate = cfg[CfgEnum.rate]
        self._running = True
        self._frames = []

    def findInternalRecordingDevice(self, p):

        for i in range(p.get_device_count()):
            devInfo = p.get_device_info_by_index(i)
            if devInfo['name'].find(TARGET) >= 0 and devInfo['hostApi'] == 0:
                return i
        return -1

    def start(self):
        threading._start_new_thread(self.__record, ())

    def __record(self):
        # === sound input setup ===
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        dev_idx = self.findInternalRecordingDevice(p)
        if dev_idx < 0:
            return
    
        stream = p.open(input_device_index=dev_idx,
                        format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chucnk)
        
        # === loop over internal sound ===
        while (self._running):
            data = stream.read(self.chucnk)
            self._frames.append(data)
            
            # === sound to text ===
            

            # === text to text ===


            # === text to subtitle ===


        stream.stop_stream()
        stream.close()
        p.terminate()
        return

    def stop(self):
        self._running = False
    
    def save(self, wav_path):
        p = pyaudio.PyAudio()
        wf = wave.open(wav_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        p.terminate()

        # === debug ===
        print("start access api")
        aai.settings.api_key = "6ea73535df834863afd8815e58563f13"
        transcriber = aai.Transcriber()
        print("finish access api")
        # transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
        transcript = transcriber.transcribe(wav_path)
        print(transcript.text)


    
class SoundToSubTitle(object):
    def __init__(self, cfg):
        self.cfg = cfg
        
    def main(self):
        pass

    def process(self):

        # === read sound ===
        input_key = input('press {} to start: '.format(self.cfg[CfgEnum.start_key]))
        if input_key == self.cfg[CfgEnum.start_key]:
            recorder = Recorder(self.cfg)
            recorder.start() # loop over internal sound

            running = True
            while running:
                input_key = input('press {} to stop: '.format(self.cfg[CfgEnum.stop_key]))
                if input_key == self.cfg[CfgEnum.stop_key]:
                    running = False
                    recorder.stop()

                    # === debug ===
                    wav_path = "record/rec_v1.wav"
                    recorder.save(wav_path)


def sound_to_text():
    pass


def read_cfg(file_path):
    with open(file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    
    return yaml_data


class CfgEnum(str, Enum):
    samplerate = "samplerate"
    duration = "duration"
    n_channels = "n_channels"
    start_key = "start_key"
    stop_key = "stop_key"
    rate = "rate"
    chucnk = "chucnk"