import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import time

import playsound
import speech_recognition as sr
#from webdriver_manager.chrome import ChromeDriverManager
import os

class VoiceRecognition:

    def __init__(self):

        self.language = 'vi'
        #self.path = ChromeDriverManager().install()
        # self.source = sr.Microphone()
        # print(self.source)
        self.recognizer = sr.Recognizer()
        self.text = []
        self.audio_array = []
        self.list_of_text = ['']

    def setup_listening_queue(self):
        self.listen_audio()
        threading.Thread(target=self.thread_recognize).start()

    def callback(self, recognizer, audio):
        self.audio_array.append(audio)

    def thread_recognize(self):
        while True:
            if self.audio_array:
                for index, audio in enumerate(self.audio_array):
                    try:
                        text = self.recognizer.recognize_google(audio, language="vi-VN")
                        self.list_of_text.append(text.lower())
                        del (self.audio_array[index])
                    except:
                        del (self.audio_array[index])

    def listen_audio(self):
        self.recognizer.listen_in_background(sr.Microphone(), self.callback, 3)

    def text_recognition(self):
        text = None
        start = time.time()
        r = sr.Recognizer()
        print("Step 1: ", time.time() - start)
        with sr.Microphone() as source:
            # self.recognizer.adjust_for_ambient_noise(source, 1)
            print("Step 2: ", time.time() - start)
            print("Tôi: ", end='')
            audio = r.listen(source, phrase_time_limit=0.5)
            print("Step 3: ", time.time() - start)

            try:
                text = r.recognize_google(audio, language="vi-VN")
                print("Step 4: ", time.time() - start)
            except:
                print("...")
        if text:
            print("Step 5: ", time.time() - start)
            return text.lower()
        else:
            return ""

    def play_audio_file(self, file):
        print(os.path.abspath("voice/anh_can_em_giup_gi_a.mp"))
        playsound.playsound(os.path.abspath(""+file))

if __name__ == "__main__":

    voice = VoiceRecognition()
    voice.play_audio_file("asd")
    # voice.setup_listening_queue()
    # while True:
    #     text = voice.list_of_text[-1]
    #     print("ok")
    #     print(text)

