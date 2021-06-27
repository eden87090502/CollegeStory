import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
from warnings import showwarning
from SPARQLWrapper import SPARQLWrapper, JSON
import pygame
from pygame.locals import*
import random
from random import choice

# 音樂播放器
pygame.init()
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
    resultStr = result["o"]["value"]
    resultList.append(resultStr)

# period
sparql = SPARQLWrapper("http://45.79.76.241:9999/blazegraph/sparql")
sparql.setQuery("""
    prefix :<http://CollegeStory.com/>
    SELECT ?period WHERE {
    ?s a :Period;
        :name ?period
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
periodList = []

for result in results["results"]["bindings"]:
    periodStr = result["period"]["value"]
    periodList.append(periodStr)

# people
sparql = SPARQLWrapper("http://45.79.76.241:9999/blazegraph/sparql")
sparql.setQuery("""
    prefix :<http://CollegeStory.com/>
    SELECT ?person WHERE {
    ?s a :Person;
        :name ?person
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
personList = []

for result in results["results"]["bindings"]:
    personStr = result["person"]["value"]
    personList.append(personStr)
del personList[0]

# event
sparql = SPARQLWrapper("http://45.79.76.241:9999/blazegraph/sparql")
sparql.setQuery("""
    prefix :<http://CollegeStory.com/>
    SELECT ?event WHERE {
    ?s a :Event;
        :name ?event
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
eventList = []

for result in results["results"]["bindings"]:
    eventStr = result["event"]["value"]
    eventList.append(eventStr)

# 音樂播放器的暫停


def pause():
    pygame.mixer.music.pause()


# 音樂播放器
global song
song = ""


def callback(entryShow):
    global song
    list = resultList
    song = random.choice(list)
    file = ("music/" + song + ".mp3")
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    entryShow.insert(tk.END, song)
    return song

# 查看音樂更多資訊


def musicMore(song, entry_show):
    sparql = SPARQLWrapper("http://45.79.76.241:9999/blazegraph/sparql")
    sparql.setQuery("""
    prefix :<http://CollegeStory.com/>
    SELECT ?MT ?SEN ?DS WHERE {
    ?f a :MusicRecording ;
	   :name "%s" ;
	   :meaningfulTime ?MT;
       :symbolizedEvent ?SE;
       :descriptionStory ?DS.

       ?SE :name ?SEN
    }
    """ % (song))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    entryShow = []

    for result in results["results"]["bindings"]:
        entryShow.append('歌曲名稱：' + song)
        entryShow.append('meaningfulTime：'+result['MT']['value'])
        entryShow.append("symbolizedEvent："+result["SEN"]["value"])
        entryShow.append("descriptionStory：" + result["DS"]["value"])

    if entry_show != []:
        entry_show.delete(0, END)
    entry_show.insert(tk.END, entryShow)

# 確認查詢


def PeriodEvent(comboPeriod, entry_show):
    sparql.setQuery("""
     prefix :<http://CollegeStory.com/>
    SELECT ?eventName 
    WHERE {
  
	?event a :Event;
         :period ?o;
         :name ?eventName.
    ?o :name '%s' 
    }""" % (comboPeriod.get()))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    entryShowEvent = []
    for result in results["results"]["bindings"]:
        entryShowEvent.append('Event：'+result['eventName']['value'])

    if entry_show != []:
        entry_show.delete(0, END)
    entry_show.insert(tk.END, entryShowEvent)


def PersonEvent(comboPerson, entry_show):
    sparql.setQuery("""
     prefix :<http://CollegeStory.com/>
    SELECT ?eventName 
    WHERE {
  
	?event a :Event;
         :attendee ?o;
         :name ?eventName.
    ?o :name '%s' 
    }""" % (comboPerson.get()))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    entryShowEvent = []
    for result in results["results"]["bindings"]:
        entryShowEvent.append('Event：'+result['eventName']['value'])

    if entry_show != []:
        entry_show.delete(0, END)
    entry_show.insert(tk.END, entryShowEvent)


def eventEvent(comboEvent, entry_show):
    sparql = SPARQLWrapper("http://45.79.76.241:9999/blazegraph/sparql")
    sparql.setQuery("""
    prefix :<http://CollegeStory.com/>
    SELECT ?pName ?aName ?des WHERE {
    ?f a :Event ;
	   :name "%s" ;
       :period ?p;
       :attendee ?a;
       :description ?des.
       
       ?a :name ?aName.
       ?p :name ?pName.
    }
    """ % (comboEvent.get()))

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    entryShowEvent = []

    for result in results["results"]["bindings"]:
        entryShowEvent.append('event：' + comboEvent.get())
        entryShowEvent.append('period：'+result['pName']['value'])
        entryShowEvent.append("attendee："+result["aName"]["value"])
        entryShowEvent.append("description：" + result["des"]["value"])

    if entry_show != []:
        entry_show.delete(0, END)
    entry_show.insert(tk.END, entryShowEvent)


def sureSong(comboSong, entry_show):
    Song = comboSong.get()
    if entry_show != []:
        entry_show.delete(0, END)
    musicMore(Song, entry_show)


def surePeriod(comboPeriod, entry_show):
    if entry_show != []:
        entry_show.delete(0, END)
    PeriodEvent(comboPeriod, entry_show)


def surePerson(comboPerson, entry_show):
    if entry_show != []:
        entry_show.delete(0, END)
    PersonEvent(comboPerson, entry_show)


def sureEvent(comboEvent, entry_show):
    if entry_show != []:
        entry_show.delete(0, END)
    eventEvent(comboEvent, entry_show)


def re(comboPeriod, comboPerson, comboEvent, comboSong, entry_show):
    entry_show.delete(0, END)
    comboSong.current()
    comboEvent.current()
    comboPerson.current()
    comboPeriod.current()

# 主頁面


def myGUI():
    root = tk.Tk()

    bgColor = "#58B2DC"
    labelColor = "#F8C3CD"
    buttonColor = "#1E88A8"
    entryColor = "#81C7D4"

    root.title("CollegeStory  2017.9 ~ 2018.7")
    root.geometry("600x650+680+0")
    root.iconbitmap("college.ico")
    root.resizable(False, False)
    root.attributes("-topmost", 1)
    root.configure(background=bgColor)

    # 標題
    labelTitle = Label(root, text="CollegeStory",
                       bg=bgColor, fg="#113285", font=('Noto Sans Mono CJK JP', 40, 'bold'))
    labelTitle.grid(row=1, column=0, sticky=W, ipadx=50, pady=12)

    # 副標題
    labelTitle = Label(root, text="2017.9 ~2018.7",
                       bg=bgColor, fg="#113285", font=('Noto Sans Mono CJK JP', 15, 'italic'))
    labelTitle.grid(row=1, column=1, sticky=W, pady=18)

    # 使用說明
    longtext = """  
    【使用說明】
    1. Demo版本，仍在測試
    2. 可以依照 Period , Person ,
     Event ,MusicRecording做查詢
    3. 選擇完參數後按下方確認鍵
    """
    labelTitle = Label(root, text=longtext, anchor='center', width=48, height=6,
                       bg=entryColor, fg="black", font=('Noto Sans Mono CJK JP', 15))
    labelTitle.grid(row=2, column=0, columnspan=2, padx=20, ipadx=12, pady=0)

    # 音樂播放
    entryShow = Entry(root, justify="center", bg=entryColor)
    entryShow.grid(row=3, column=0, columnspan=2, sticky=W, padx=20,
                   pady=12, ipadx=210, ipady=24)

    buttonPause = Button(root, text="Pause", bg=buttonColor,
                         width=10, heigh=3, command=lambda: pause())
    buttonPause.grid(row=3, column=0, columnspan=2,
                     sticky=E, padx=120)

    buttonMore = Button(root, text="歌曲資訊", bg=buttonColor, width=10,
                        heigh=3, command=lambda: musicMore(song, entry_show))
    buttonMore.grid(row=3, column=0, columnspan=2, sticky=E,
                    padx=30)

    # 選擇時期
    label2 = Label(root, text="選擇時期", width=8,
                   height=2, bg=labelColor, font=('Noto Sans Mono CJK JP', 8))
    label2.grid(row=4, column=0, columnspan=2, sticky=W, padx=20, pady=15)

    comboPeriod = ttk.Combobox(
        root, values=periodList)
    comboPeriod.grid(row=4, column=0,
                     sticky=W, padx=79, pady=15)
    comboPeriod.current()

    buttonPeriodSure = Button(root, text="確認查詢", bg=buttonColor, width=8,
                              height=1, font=('Noto Sans Mono CJK JP', 8), command=lambda: surePeriod(comboPeriod, entry_show))
    buttonPeriodSure.grid(row=4, column=0, columnspan=2,
                          sticky=W, pady=15, padx=248)

    # 選擇人物
    label2 = Label(root, text="選擇人物", width=8,
                   height=2, bg=labelColor, font=('Noto Sans Mono CJK JP', 8))
    label2.grid(row=4, column=0, columnspan=2, sticky=E, padx=240, pady=15)

    comboPerson = ttk.Combobox(
        root, values=personList)
    comboPerson.grid(row=4, column=0, columnspan=2, sticky=E, padx=76, pady=15)
    comboPerson.current()
    buttonPersonSure = Button(root, text="確認查詢", bg=buttonColor, width=8,
                              height=1, font=('Noto Sans Mono CJK JP', 8), command=lambda: surePerson(comboPerson, entry_show))
    buttonPersonSure.grid(row=4, column=0, columnspan=2,
                          sticky=E, pady=15, padx=15)

    # 選擇事件
    label2 = Label(root, text="選擇事件", width=8,
                   height=2, bg=labelColor, font=('Noto Sans Mono CJK JP', 8))
    label2.grid(row=5, column=0, columnspan=2, sticky=W, padx=20, pady=15)

    comboEvent = ttk.Combobox(
        root, values=eventList)
    comboEvent.grid(row=5, column=0,
                    sticky=W, padx=79, pady=15)
    comboEvent.current()
    buttonEventSure = Button(root, text="確認查詢", bg=buttonColor, width=8,
                             height=1, font=('Noto Sans Mono CJK JP', 8), command=lambda: sureEvent(comboEvent, entry_show))
    buttonEventSure.grid(row=5, column=0, columnspan=2,
                         sticky=W, pady=15, padx=248)

    # 選擇歌曲
    label2 = Label(root, text="選擇歌曲", width=8,
                   height=2, bg=labelColor, font=('Noto Sans Mono CJK JP', 8))
    label2.grid(row=5, column=0, columnspan=2, sticky=E, padx=240, pady=15)

    comboSong = ttk.Combobox(
        root, values=resultList)
    comboSong.grid(row=5, column=0, columnspan=2, sticky=E, padx=76, pady=15)
    comboSong.current()
    buttonSongSure = Button(root, text="確認查詢", bg=buttonColor, width=8,
                            height=1, font=('Noto Sans Mono CJK JP', 8), command=lambda: sureSong(comboSong, entry_show))
    buttonSongSure.grid(row=5, column=0, columnspan=2,
                        sticky=E, pady=15, padx=15)

    # 重新輸入
    button_re = Button(root, text="重新查詢", bg=buttonColor, width=18,
                       height=1, font=('Noto Sans Mono CJK JP', 13), command=lambda: re(comboPeriod, comboPerson, comboEvent, comboSong, entry_show))
    button_re.grid(row=6, column=0, columnspan=80,
                   sticky=W, pady=15, padx=220)

    # 顯示狀態列
    entry_show = Entry(root, justify="center", bg=entryColor)
    entry_show.grid(row=7, column=0, columnspan=80, sticky=W, padx=20,
                    pady=10, ipadx=210, ipady=40)

    # 創作者標示
    labelName = Label(root, text="made by Deng Tai - 2021.6",
                      bg=bgColor, font=('Yu Gothic UI Semilight', 8))
    labelName.place(x=230, y=630)

    callback(entryShow)
    root.mainloop()


myGUI()
