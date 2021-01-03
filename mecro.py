from tkinter.constants import LEFT, NORMAL, RIGHT
import keyboard
import tkinter
import time
import threading

isstart=False
chack=False
st=False
lists=[]
keys={}
dic2={}
num=0

#event함수
def event(key):
    global isstart
    global chack
    global lists
    global keys
    global num
    if not chack:
        if key.name=="f8":
            isstart=True
            text.delete(1.0, tkinter.END)
            text.insert(1.0, "시작됨")
        if key.name=="f9":
            isstart=False
            text.delete(1.0, tkinter.END)
            text.insert(1.0, "중지됨")
        if key.name=="f10":
            text.delete(1.0, tkinter.END)
            text.insert(1.0, "\n".join(map(lambda s:str(s), lists[1:])))
    if chack:
        if key.event_type=="up":
            num=time.time()
            lists.append(key.time-keys[key.name]["time"])
            lists.append(key.name)
            del keys[key.name]
        else:
            if keys.get(key.name, 0)==0:
                lists.append(time.time()-num)
                lists.append(key.name)
                keys[key.name]={"event":"down", "time":key.time}

#키보드 눌렸을때 event함수 실행
keyboard.hook(event)

#기록 시작/중지 체인지
def change():
    global chack
    global lists
    if chack:
        chack=False
        text.delete(1.0, tkinter.END)
        text.insert(1.0, "기록 중지됨")
    else:
        lists=[]
        chack=True
        text.delete(1.0, tkinter.END)
        text.insert(1.0, "기록 시작됨")

#gui
gui=tkinter.Tk()
gui.geometry("1000x270")
gui.title("simple mecro")
gui.resizable(False, False)

tkinter.Button(gui, text="기록 시작", pady=50, padx=50, command=change).pack(side=LEFT)
tkinter.Button(gui, text="기록 중지", pady=50, padx=50, command=change).pack(side=LEFT)
text=tkinter.Text(gui, state=NORMAL)
text.insert(1.0, "여기에 문구가 표시됩니다.")
text.pack(side=RIGHT)

#키보드 반복동작 함수
def loop():
    global lists
    global isstart
    global st
    while True:
        if isstart and not st:
            st=True
            for i in lists[1:]:
                if type(i)==str:
                    if not dic2.get(i, False):
                        keyboard.press(i)
                        dic2[i]=True
                    else:
                        del dic2[i]
                        keyboard.release(i)
                else:
                    time.sleep(i)
            #모든 동작 누르기 취소
            for i in lists[1:]:
                if type(i)==str:
                    keyboard.release(i)
            st=False
            time.sleep(0.4)

#키보드 반복동작 쓰레딩
t=threading.Thread(target=loop)
t.daemon=True
t.start()

#gui루핑
gui.mainloop()