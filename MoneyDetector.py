## -*- coding: utf-8 -*-

import cv2
# import cv2.data
font = cv2.FONT_ITALIC

from imutils.video import FileVideoStream
from imutils.video import VideoStream
import imutils
import time, os

from Utils import *

import CCamera_Function



class MoneyDetector(CCamera_Function.CCamera_Function):

    def __init__(self):
        super().__init__()
        print("__INIT__ MoneyDetector")

        if os.name == 'nt':
            self.MD_RESOURCE_DIR = "../md_resource/"
        else:
            self.MD_RESOURCE_DIR = "/home/pi/md_resource/"

        self.SaveImagePath = self.MD_RESOURCE_DIR + "capture_save/"  # 이미지 저장할 경로
        self.READ_PICTURE_PATH = self.MD_RESOURCE_DIR + "capture/"   # 읽어올 이미지 경로
        self.VIDEO_PATH = self.MD_RESOURCE_DIR + "video/video_omanf.mp4"  # 비디오 경로 및 파일이름


        self.cascade_money_list = ["cascade_chunwon", "cascade_ochunwon", "cascade_manwon", "cascade_omanwon", "cascade_chunwon_b", "cascade_ochunwon_b", "cascade_manwon_b", "cascade_omanwon_b"]

    def Sound_play(self, filename):

        # aplay sound-0.wav
        import os

        if os.name == 'nt':
            print ("FAKE SOUND PLAY: ", filename)
        else:

            # os.system('aplay output.wav')
            # cmd = 'aplay ' + filename + ".WAV"
            cmd = 'aplay ' + self.MD_RESOURCE_DIR+'wav/'+filename+'.wav'
            print (cmd)
            # os.system('aplay black.wav')

            os.system(cmd)
            # os.system("vlc C:\\link\\test_character_learn\\black.mp3") # not work on windows

            # os.system("vlc C:/link/test_character_learn/black.mp3")

    def DetectCascade(self, frame):  # override method

        cascade_list = self.cascade_money_list

        # frame = imutils.resize(frame, width=450)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(gray,1.3, 5)
        for ix, cscd in enumerate(cascade_list):
            
            cascade_filename = self.MD_RESOURCE_DIR+'cascade/'+cscd+".xml"
            #print (cascade_filename)
            cascade = cv2.CascadeClassifier(cascade_filename)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detect = cascade.detectMultiScale(gray,1.3, 5)

            if len(detect) == 1:


                print ("detected: ", cscd)


                cv2.putText(frame, u"Image Recognition", (5,15), font, 0.5, (255,255, 255),1)


                for(x,y, w,h) in detect:

                    nx = x
                    ny = y+int(h*0.3)
                    nw = x+w
                    nh = ny+int(w*0.5)

                    # cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)  #사각형 범위
                    cv2.rectangle(frame, (nx,ny), (nw, nh), (255,0,0), 2)  #사각형 범위

                    cut_frame = frame[ny:nh, nx:nw]
                    ret_color = self.get_hsv(cut_frame)



                    if ix == 0:
                        detect_money = "1000"
                    elif ix == 1:
                        detect_money = "5000"
                    elif ix == 2:
                        detect_money = "10000"
                    else:
                        detect_money = "50000"

                    print (cscd)
                    ret_str = cscd.split('_')
                    ret_str = ret_str[1]

                    if ret_str == 'chunwon':
                        detect_money = "1000"
                    elif ret_str == 'ochunwon':
                        detect_money = "5000"
                    elif ret_str == 'manwon':
                        detect_money = "10000"
                    elif ret_str == 'omanwon':
                        detect_money = "50000"


                    cv2.putText(frame, detect_money, (x-5, y-5), font, 1.5, (255,255,0),2)  #찾았다는 메시지

                    cv2.imshow("cut", cut_frame)


                    # key = cv2.waitKey(1) & 0xFF

                    # if the `q` key was pressed, break from the loop
                    # if key == ord("q"):
                    #     break

                    self.Sound_play(ret_str)
                    break



if __name__ == "__main__":

    obj = MoneyDetector()
    obj.APP_MAIN()

