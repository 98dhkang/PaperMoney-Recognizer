#!/usr/bin/python
# -*- coding: utf-8 -*

def getFilesFromDirectory(ext, path):
    import os
    FileList = []

    for file in os.listdir(path):
        if file.endswith("."+ext):
            FileList.append(file)

    return FileList
    # mp4_name = os.path.join( os.getcwd() , "resource" ,goal_mp4_files[random.randrange(0,len(goal_mp4_files))])
    # mp4_name = goal_mp4_files[random.randrange(0,len(goal_mp4_files))]
    # name = "C:\kprj\dev\K190612_DroneDetect\src\python\pyqt_test\example\goal.mp4"
    # name = "./resource/goal.mp4"
    # print mp4_name
