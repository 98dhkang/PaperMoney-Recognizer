#!/usr/bin/python
# -*- coding: utf-8 -*


# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
#import dlib
import cv2
#from CSoundOutput import *
import time
import os
# from Utils import *
import Dir_Utils
import CV_Utils


class CCamera_Function:
    def __init__(self):
        print ("__init__")

        # self.TAKE_PICTURE_FROM = "IMAGE"
        #self.TAKE_PICTURE_FROM = "VIDEO"
        self.TAKE_PICTURE_FROM = "CAMERA"

        # self.ParseArgument()

        self.bSaveImage = False # 이미지 저장할지

        if os.name == 'nt':
            self.SaveImagePath = "./capture_save/"  # 이미지 저장할 경로
            self.READ_PICTURE_PATH = "./capture/"        # 읽어올 이미지 경로
            self.VIDEO_PATH = "./20191015_154822.mp4"  # 비디오 경로


        else:
            self.SaveImagePath = "/home/pi/capture_save/"
            self.READ_PICTURE_PATH = "./capture/"
            self.VIDEO_PATH = "./capture_chunwon_b.mp4"


        self.eye_detect = False
        self.font = cv2.FONT_ITALIC

        self.face_cascade = cv2.CascadeClassifier("cascade_chunwon_b_envy.xml")

        self.CAM_WIDTH = 640
        self.CAM_HEIGHT = 480
        self.font = cv2.FONT_ITALIC



    def DetectCascade(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray,1.3, 5)

        for(x,y, w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)  #사각형 범위
            cv2.putText(frame, "Detected", (x-5, y-5), self.font, 0.5, (255,255,0),2)  #얼굴찾았다는 메시지
            if self.eye_detect:  #눈찾기
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)

        # cv2.imshow("frame", frame)
        k=cv2.waitKey(30)

        #실행 중 키보드 i 를 누르면 눈찾기를 on, off한다.
        if k == ord('i'):
            self.eye_detect = not self.eye_detect


    def SHOW_CAMERA(self):

        self.vs = None
        self.pictureList = None

        if os.name != 'nt':
            time.sleep(2.0) # 파이에서 돌아가는 경우 딜레이 안주면 익셉션 발생함

        #self.cam = cv2.VideoCapture(0) # 이건 파이에서 느림

        if self.TAKE_PICTURE_FROM == "VIDEO":
            self.vs = FileVideoStream(self.VIDEO_PATH).start()
        elif self.TAKE_PICTURE_FROM == "CAMERA":
            if os.name == 'nt':
                self.vs = VideoStream(usePiCamera=False).start()
            else:
                self.vs = VideoStream(usePiCamera=True).start()
        elif self.TAKE_PICTURE_FROM == "IMAGE":
            self.pictureList = []
            # loop over frames from the video stream
            self.pictureList = Dir_Utils.getFilesFromDirectory("jpg", self.READ_PICTURE_PATH)
            # print (self.pictureList)

        if os.name != 'nt':
            time.sleep(3.0) # 파이에서 돌아가는 경우 딜레이 안주면 익셉션 발생함


        frame_count = 0

        while True:
            frame_count+=1
            frame= None

            if self.TAKE_PICTURE_FROM == "IMAGE":
                if len(self.pictureList) == 0:
                    break

                pictureFile = self.pictureList.pop()
                # print(pictureFile)
                frame = cv2.imread(self.READ_PICTURE_PATH+pictureFile)
            elif self.TAKE_PICTURE_FROM == "VIDEO":
                frame = self.vs.read()
                if not self.vs.more():
                    print ("END OF FRAME")
                    break

            elif self.TAKE_PICTURE_FROM == "CAMERA":
                frame = self.vs.read()

            frame = imutils.resize(frame, width=450)
            # frame = CV_Utils.rotate_img(frame, 270)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.DetectCascade(frame)

            cv2.putText(frame, "Frame: {}".format(frame_count), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


            if self.bSaveImage == True:
                save_file_name = self.SaveImagePath + 'capture_%05d.jpg'%frame_count

                print (save_file_name)
                cv2.imwrite(save_file_name, frame)


            # show the frame
            cv2.imshow("Detecting", frame)


            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break


        # do a bit of cleanup
        cv2.destroyAllWindows()
        if self.vs != None:
            self.vs.stop()

    def ParseArgument(self):

        ap = argparse.ArgumentParser()
        # ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")
        # ap.add_argument("-v", "--video", type=str, default="", help="path to input video file")

        ap.add_argument("-t", "--test", action="store_true", default=False, help="TEST MODE")
        ap.add_argument("-v", "--video", action="store_true", default=False, help="detect from video")
        ap.add_argument("-p", "--picture", action="store_true", default=False, help="detect from picture")

        args = vars(ap.parse_args())

        # print (args["video"])
        if args["video"] == True:
            self.bFileVideoStream = True
        else:
            self.bFileVideoStream = False

        if args["test"] == True:
            self.bTestMode = True
        else:
            self.bTestMode = False

        if args["picture"] == True:
            self.bDetectFromPicture = True
            self.bTestMode = True      # only test mode can parse picture
        else:
            self.bDetectFromPicture = False


    def APP_MAIN(self):

        if os.name == 'nt':
            self.SHOW_CAMERA()
        else:
            try:
                self.SHOW_CAMERA()
            except Exception as e :
                import sys
                _, _ , tb = sys.exc_info()    # tb  ->  traceback object
                print ("EXCEPTION ###", e, "[{}]".format(__file__), "[{}]".format(tb.tb_lineno))

                # print ("EXCEPTION #################################")
                # print (e)
                # print(__file__.split("\\")[-1])
                # print ('file name = ', __file__)
                # print ('error line No = {}'.format(tb.tb_lineno))


        

if __name__ == "__main__":

    obj = CCamera_Function()
    obj.APP_MAIN()
