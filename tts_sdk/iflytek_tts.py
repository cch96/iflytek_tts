# -.- coding: utf-8 -.-
import os
import threading
import platform
from datetime import datetime
import time
import wave
import ctypes
from ctypes import CDLL, cdll, c_int, byref, string_at

WORK_ROOT = os.path.dirname(os.path.abspath(__file__))
MSC_LOAD_LIBRARY = "libs/x64/libmsc.so"
VOICE_NAME = b"xiaoyan"
LOGIN_TTS_RES_PATH = "fo|bin/msc/res/tts/xiaoyan.jet"
SESSION_TTS_RES_PATH = b"fo|bin/msc/res/tts/xiaoyan.jet;fo|bin/msc/res/tts/common.jet"


class IflytekTTS(object):
    """
    科大讯飞离线语音合成
    开发API文档：http://mscdoc.xfyun.cn/windows/api/iFlytekMSCReferenceManual/files.html
    API调用流程：https://doc.xfyun.cn/msc_windows/%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.html
    """

    MSP_SUCCESS = 0 # 成功登入返回标志

    def __new__(cls, *args, **kwargs):
        # 加载库
        ctypes.CDLL("libstdc++.so.6", mode=ctypes.RTLD_GLOBAL)
        plat = platform.architecture()
        if plat[0] == '32bit':
            dll = CDLL(os.path.join(WORK_ROOT, 'libs/x86/libmsc.so'), mode=ctypes.RTLD_GLOBAL)
        else:
            dll = CDLL(os.path.join(WORK_ROOT, 'libs/x64/libmsc.so'), mode=ctypes.RTLD_GLOBAL)
        cls.dll = cdll.LoadLibrary(os.path.join(WORK_ROOT, "libtts.so"))
        cls.lock = threading.RLock()
        return super(IflytekTTS, cls).__new__(cls)

    def __init__(self, app_id, work_dir=os.path.join(WORK_ROOT, "bin")):
        """
        :params app_id: 注册了离线语音应用后给都app_id
        :params work_dir: 工作目录默认是当前文件夹下
        """

        self.session_begin_params = self.get_session_params()
        self.login_params = "appid = %s, work_dir = %s" % (app_id, work_dir)
        # 第一个参数是用户名，第二个参数是密码，第三个参数是登录参数，用户名和密码可在http://www.xfyun.cn注册获取

    @staticmethod
    def get_session_params():
        """
        登录参数,appid与msc库绑定,请勿随意改动
        
        rdn:           合成音频数字发音方式
        volume:        合成音频的音量
        pitch:         合成音频的音调
        speed:         合成音频对应的语速
        voice_name:    合成发音人
        sample_rate:   合成音频采样率
        text_encoding: 合成文本编码格式
        """
        session_begin_params = "engine_type = local,voice_name=xiaoyan, " + \
            "text_encoding = UTF8, " + \
            "tts_res_path = fo|res/tts/xiaoyan.jet;fo|res/tts/common.jet, " + \
            "sample_rate = 16000, speed = 50, volume = 50, pitch = 50, rdn = 2" 
        return session_begin_params        

    def text2wav(self, text, filename):
	"""
        文字合成语音
	"""
        # 底层的c是不支持多线程的，所以这里限制一下
        with self.lock:
            ret = self.dll.msp_login(None, None, self.login_params)
            if (self.MSP_SUCCESS != ret):
                # 如果登陆验证失败
                print("MSPLogin failed, error code: %d.\n", ret)
                return
            #  登陆成功
            # print("开始合成 ...\n")
            ret = self.dll.text_to_speech(text, filename, self.session_begin_params)
            # print("合成完毕\n")
            # 退出登录
            self.dll.msp_logout()
        
