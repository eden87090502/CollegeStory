from SPARQLWrapper import SPARQLWrapper, JSON
from tkinter import *
from tkinter import filedialog
import pygame
from pygame.locals import*
import sys
import os
import time
import random
from random import choice


# ---遊戲初始化和窗口的定義、標題、大小設置---
pygame.init()
root = Tk()  # 窗口
root.title("音樂播放器")  # 標題
root.geometry("1000x800+400+200")  # 更改大小和位置


sparql = SPARQLWrapper("http://45.79.76.241:9999/blazegraph/sparql")
sparql.setQuery("""
    prefix :<http://CollegeStory.com/>
    SELECT ?o WHERE {
    ?s a :MusicRecording;
        :name ?o
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
resultList = []

for result in results["results"]["bindings"]:
    # print(result["o"]["value"])
    resultStr = result["o"]["value"]
    resultList.append(resultStr)
print(resultList)


def pause():
    pygame.mixer.music.pause()


def stop():
    pygame.mixer.music.stop()


def start():
    pygame.mixer.music.unpause()


def callback():
    list = resultList
    # list = ["好好%20(想把你寫成一首歌)", "妳", "一事無成的偉大",
    #         "我還年輕我還年輕", "追光者", "兄弟沒夢不應該",
    #         "我喜歡你", "我的事不關你的事%20Not%20Your%20Business", "閃退%20Flash%20Back",
    #         "爛泥", "夜空中最亮的星", "學著習慣", "我想聽你聲音%20Listen%20To%20Your%20Voice"
    #         ]

    # song = random.choice(list)
    # file = ("music/" + song + ".mp3")
    # pygame.mixer.init()
    # track = pygame.mixer.music.load(file)
    # pygame.mixer.music.play()

    song = random.choice(list)
    file = ("music/" + song + ".mp3")
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    song1 = random.choice(list)
    file = ("music/" + song1 + ".mp3")
    pygame.mixer.init()
    pygame.mixer.music.queue(file)


# ---按鈕設置：位置、名字、命令功能等
b = Button(root, text="選擇音樂", bg='yellow', command=callback)
b.place(x=10, y=10)
f = Button(root, text="暫停", bg='yellow', command=pause)
f.place(x=10, y=50)
bs = Button(root, text="繼續", bg='yellow', command=start)
bs.place(x=10, y=90)
bst = Button(root, text="停止", bg='yellow', command=stop)
bst.place(x=10, y=130)
l = Label(root, text="歡迎來到自定義音樂播放器！", bg='pink', fg='blue')
l.place(x=10, y=180)

callback()

root.mainloop()
