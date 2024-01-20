import yaml
import wave
import pyaudio
import threading
from enum import Enum
import speech_recognition as sr

TARGET = "立體聲混音"

class Recorder(object):
    def __init__(self, cfg):
        self.chucnk = cfg[CfgEnum.chucnk]
        self.format = pyaudio.paInt16
        self.channels = cfg[CfgEnum.n_channels]
        self.rate = cfg[CfgEnum.rate]
        self._running = True
        self._frames = []
        self.recognizer = sr.Recognizer()
        self.cfg = cfg
        self.p = pyaudio.PyAudio()
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
        
        dev_idx = self.findInternalRecordingDevice(self.p)
        if dev_idx < 0:
            return
    
        stream = self.p.open(input_device_index=dev_idx,
                        format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chucnk)
        
        # === loop over internal sound ===
        while (self._running):
            # data = stream.read(self.chucnk)
            data = stream.read(self.rate * 5)

            # self._frames.append(data)
            try:
                audio_data_instance = sr.AudioData(data, 44100, 2)
                print(self.recognizer.recognize_google(audio_data_instance, show_all=False))
            # === sound to text ===
            except:
                pass

            # === text to text ===


            # === text to subtitle ===


        stream.stop_stream()
        stream.close()
        self.p.terminate()

        return

    def stop(self):
        self._running = False
    


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