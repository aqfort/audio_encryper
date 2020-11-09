import wave
import numpy as np


class Audio:
    def __init__(self, frame=None, pararms=None, filename=None):
        self.params = pararms
        self.frame = frame
        if filename is not None:
            self.params, self.frame = self.read_audio_file(filename)

    @staticmethod
    def read_audio_file(filename, n=None):
        wave_read = wave.open(filename, "rb")
        if n is None:
            n = wave_read.getnframes()
        params = wave_read.getparams()
        frame = np.copy(wave_read.readframes(n))
        frame = np.frombuffer(frame, dtype=np.int16)
        wave_read.close()
        return params, frame

    def write_to_file(self, frame, name):
        wave_write = wave.open(name, "wb")
        wave_write.setparams(self.params)
        wave_write.writeframes(frame)
        wave_write.close()

    def __str__(self):
        return"""
frame head: {}
parameters: {}""".format(self.frame[0:15], self.params)
