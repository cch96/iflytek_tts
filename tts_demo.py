# -.- coding: utf-8 -.-

from tts_sdk.iflytek_tts import IflytekTTS
import time

content = "你好吗哈哈哈哈哈"
APP_ID = "5d5fa70d"

tts = IflytekTTS(APP_ID)
t1 = time.time()
tts.text2wav(content, "demo.wav")
print time.time() - t1 
