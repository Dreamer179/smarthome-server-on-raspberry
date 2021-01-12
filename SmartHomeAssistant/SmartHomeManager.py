#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on deploy stage 2"
__version__ = "2020.10.17"

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ctypes
import datetime
import json
import os
import re
import smtplib
import urllib.request as urllib2
import webbrowser
from time import strftime

import playsound
import requests
import wikipedia
from gtts import gTTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from youtube_search import YoutubeSearch

from SmartHomeAssistant.VoiceRecognition import VoiceRecognition
from SmartHomeDevice.ESPCommunication import ESPCommunication
from UltilitiesAndMacro import *
wikipedia.set_lang('vi')

class SmartHomeManager(VoiceRecognition):

    def __init__(self):
        super().__init__()
        self.device_communication = ESPCommunication.getInstance()
        self.setup_listening_queue()

    def assistant_annoucement_speak(self, text):
        print("Bot: {}".format(text))
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save("sound.mp3")
        playsound.playsound("sound.mp3")
        print('Annoucement complete!')
        os.remove("sound.mp3")

    def assistant_greeting(self):
        day_time = int(strftime('%H'))
        if day_time < 12:
            self.play_audio_file("voice/chao_buoi_sang.mp3")
        elif 12 <= day_time < 18:
            self.play_audio_file("voice/chao_buoi_chieu.mp3")
        else:
            self.play_audio_file("voice/chao_buoi_toi.mp3")

    def assistant_get_date_and_time(self, text):

        now = datetime.datetime.now()
        if "giờ" in text:
            self.assistant_annoucement_speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
        elif "ngày" in text:
            self.assistant_annoucement_speak("Hôm nay là ngày %d tháng %d năm %d" %
                                       (now.day, now.month, now.year))
        else:
            self.assistant_annoucement_speak("Bot chưa hiểu ý của anh. anh nói lại được không?")


    def assistant_open_application(self, text):

        if "google" in text:
            self.assistant_annoucement_speak("Mở Google Chrome")
            os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        elif "word" in text:
            self.assistant_annoucement_speak("Mở Microsoft Word")
            os.startfile('C:\Program Files\Microsoft Office\\root\Office16\\WINWORD.EXE')
        elif "excel" in text:
            self.assistant_annoucement_speak("Mở Microsoft Excel")
            os.startfile('C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE')
        elif "access" in text:
            self.assistant_annoucement_speak("Mở Microsoft Excel")
            os.startfile('C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE')
        else:
            self.assistant_annoucement_speak("Ứng dụng chưa được cài đặt. anh hãy thử lại!")


    def assistant_open_website(self, text):

        reg_ex = re.search('mở (.+)', text)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            self.assistant_annoucement_speak("Trang web anh yêu cầu đã được mở.")
            return True
        else:
            return False

    def assistant_open_google_and_search(self, text):

        search_for = text.split("kiếm", 1)[1]
        self.assistant_annoucement_speak('Okay!')
        driver = webdriver.Chrome(self.path)
        driver.get("http://www.google.com")
        que = driver.find_element_by_xpath("//input[@name='q']")
        que.send_keys(str(search_for))
        que.send_keys(Keys.RETURN)

    def assistant_send_email(self, text):
        self.assistant_annoucement_speak('anh gửi email cho ai nhỉ')
        recipient = self.text_recognition()
        if 'yến' in recipient:
            self.assistant_annoucement_speak('Nội dung anh muốn gửi là gì')
            content = self.text_recognition()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('luongngochungcntt@gmail.com', 'hung23081997')
            mail.sendmail('luongngochungcntt@gmail.com',
                          'hungdhv97@gmail.com', content.encode('utf-8'))
            mail.close()
            self.assistant_annoucement_speak('Email của anh vùa được gửi. anh check lại email nhé hihi.')
        else:
            self.assistant_annoucement_speak('Bot không hiểu anh muốn gửi email cho ai. anh nói lại được không?')

    def assistant_get_current_weather(self):

        self.play_audio_file("voice/anh_muon_xem_thoi_tiet_o_dau_a.mp3")
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        city = self.text_recognition()
        if not city:
            pass
        api_key = "fe8d8c65cf345889139d8e545f57819a"
        call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
        response = requests.get(call_url)
        data = response.json()
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            weather_description = wthr[0]["description"]
            now = datetime.datetime.now()
            content = """
            Hôm nay là ngày {day} tháng {month} năm {year}
            Mặt trời mọc vào {hourrise} giờ {minrise} phút
            Mặt trời lặn vào {hourset} giờ {minset} phút
            Nhiệt độ trung bình là {temp} độ C
            Áp suất không khí là {pressure} héc tơ Pascal
            Độ ẩm là {humidity}%
            Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                               hourset = sunset.hour, minset = sunset.minute,
                                                                               temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
            self.assistant_annoucement_speak(content)
        else:
            self.assistant_annoucement_speak("Không tìm thấy địa chỉ của anh")

    def assistant_play_song(self):
        self.play_audio_file("voice/anh_chon_ten_bai_hat_di_a.mp3")
        mysong = self.text_recognition()
        while True:
            result = YoutubeSearch(mysong, max_results=10).to_dict()
            if result:
                print(result.shape)
                break
        url = 'https://www.youtube.com' + result[0]['channel_link']
        webbrowser.open(url)
        self.assistant_annoucement_speak("Bài hát anh yêu cầu đã được mở.")

    def assistant_change_wallpaper(self):
        api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
        url = 'https://api.unsplash.com/photos/random?client_id=' + \
            api_key  # pic from unspalsh.com
        f = urllib2.urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        # Location where we download the image to.
        urllib2.urlretrieve(photo, "C:/Users/Night Fury/Downloads/a.png")
        image=os.path.join("C:/Users/Night Fury/Downloads/a.png")
        ctypes.windll.user32.SystemParametersInfoW(20,0,image,3)
        self.assistant_annoucement_speak('Hình nền máy tính vừa được thay đổi')


    def assistant_read_news(self):
        self.play_audio_file("voice/anh_muon_doc_bao_ve_gi_a.mp3")

        queue = self.text_recognition()
        params = {
            'apiKey': '30d02d187f7140faacf9ccd27a1441ad',
            "q": queue,
        }
        api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
        api_response = api_result.json()
        print("Tin tức")

        for number, result in enumerate(api_response['articles'], start=1):
            print(f"""Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}
        """)
            if number <= 3:
                webbrowser.open(result['url'])

    def assistant_tell_me_about(self):
        try:
            self.play_audio_file("voice/anh_muon_nghe_ve_gi_a.mp3")
            text = self.text_recognition()
            contents = wikipedia.summary(text).split('\n')
            self.assistant_annoucement_speak(contents[0])
            for content in contents[1:]:
                self.play_audio_file("voice/anh_muon_nghe_them_khong_a.mp3")
                ans = self.text_recognition()
                if "có" not in ans:
                    break
                self.assistant_annoucement_speak(content)

            self.play_audio_file("voice/anh_can_em_giup_gi_a.mp3")
        except:
            self.play_audio_file("voice/em_tim_chua_thay_a.mp3")

    def assistant_help_me(self):
        self.play_audio_file("voice/thong_tin.mp3")

    def assistant_turn_on_led(self):
        command = "ON"
        self.device_communication.broadcast_all_device(command)
        return command

    def assistant_turn_off_led(self):
        command = "OFF"

        self.device_communication.broadcast_all_device(command)
        return command

    def assistant_turn_on_led_single(self, device_id, command):
        command_json = {"device_id": "1",
                        "device_name": device_id,
                        "device_command": command
                        }
        self.device_communication.broadcast_single_device(command_json)
        return command

    def assistant_turn_off_led_single(self, device_name, command):
        command = {"device_id": "1",
                   "device_name": device_name,
                   "device_command": command
                   }
        self.device_communication.broadcast_single_device(command)
        return command

    def assistant_main_assist(self):
        running = True
        os.path.abspath("SmartHomeAssistant/voice/gioi_thieu.mp3")
        # self.play_audio_file(os.path.abspath("SmartHomeAssistant/voice/gioi_thieu.mp3"))
        self.play_audio_file("voice/gioi_thieu.mp3")

        while running:
            print("Running")
            name = self.list_of_text[-1]
            if "trợ lý" in name or "clip" in name:
                print("LISTENINHG")
                self.play_audio_file("voice/anh_can_em_giup_gi_a.mp3")
                self.list_of_text = [""]
                while True:
                    text = self.list_of_text[-1]
                    print(text)
                    if "bật đèn" in text or "mở điện" in text or "bật điện" in text or "mở đèn" in text:
                        print("em bật đèn đây")
                        if "phòng ngủ" in text:
                            print("em bật đèn phòng ngủ đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_on_led_single("PHONG_NGU", "ON")
                        elif "phòng khách" in text:
                            print("em bật đèn phòng khách đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_on_led_single("PHONG_KHACH", "ON")
                        elif "phòng vệ sinh" in text:
                            print("em bật đèn phòng khách đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_on_led_single("PHONG_VE_SINH", "ON")
                        else:
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_on_led()
                        break

                    elif "đổi màu" in text:
                        # if "phòng ngủ" in text:
                        if "đổi màu trắng" in text:
                            print("em đổi màu đèn phòng khách đây");
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_on_led_single("PHONG_NGU", "WHITE")
                            break
                        elif "đổi màu vàng" in text:
                            print("em đổi màu đèn phòng khách đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_on_led_single("PHONG_NGU", "YELLOW")
                            break

                        elif "đổi màu cam" in text:
                            print("em đổi màu đèn phòng khách đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_on_led_single("PHONG_NGU", "ORANGE")
                            break

                    elif "tắt đèn" in text or "tắt điện" in text:
                        print("em tắt đèn đây")
                        if "phòng ngủ" in text:
                            print("em tắt đèn phòng ngủ đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_off_led_single("PHONG_NGU", "OFF")
                        elif "phòng khách" in text:
                            print("em tắt đèn phòng khách đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_off_led_single("PHONG_KHACH", "OFF")
                        elif "phòng vệ sinh" in text:
                            print("em tắt đèn phòng vệ sinh đây")
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_off_led_single("PHONG_VE_SINH", "OFF")
                        else:
                            self.play_audio_file("voice/em_lam_ngay_day_a.mp3")
                            self.assistant_turn_off_led()
                        break

                    elif "dừng" in text or "tạm biệt" in text or "ngủ thôi" in text:
                        self.play_audio_file("voice/hen_gap_lai_anh_sau_a.mp3")
                        running = False
                        break

                    elif "có thể làm gì" in text:
                        self.assistant_help_me()
                        break

                    elif "chào trợ lý ảo" in text:
                        self.assistant_greeting()
                        break

                    elif "hiện tại" in text:
                        self.assistant_get_date_and_time(text)
                        break

                    elif "tìm kiếm" in text:
                        if 'google' in text:
                            self.assistant_open_google_and_search(text)
                        elif "." in text:
                            self.assistant_open_website(text)
                        else:
                            self.assistant_open_application(text)
                        break

                    elif "email" in text or "mail" in text or "gmail" in text:
                        self.assistant_send_email(text)
                        break

                    elif "thời tiết" in text:
                        self.assistant_get_current_weather()
                        break

                    elif "mở nhạc" in text:
                        self.assistant_play_song()
                        break

                    elif "hình nền" in text:
                        self.assistant_change_wallpaper()
                        break

                    elif "đọc báo" in text:
                        self.assistant_read_news()
                        break

if __name__ == "__main__":
    friday = SmartHomeManager()
    friday.assistant_turn_off_led_single("PHONG_NGU", "ON")
            