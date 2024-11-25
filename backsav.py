#本来想用cpp写 重温一下MFC，但是这里网太差了下不了kit
#一代cpp高手陨落，sorry！
import os
import time
import shutil
import tkinter
from pynput.keyboard import Key
from pynput import keyboard
import json
import threading

jl=json.load(open("settings.json",encoding="utf8"))
FILES=jl["file"] 
files_lt={}
CDIR=jl["dir"]
CMOST_BACK_FILE=jl["max_files"] #最大备份文件数量
MANUAL_FILES=jl["manual_file"]

def daemon():
    while True:
        for i in FILES:
            bdir=os.path.dirname(i)+CDIR
            realname=os.path.basename(i).split(".")[0]
            if os.path.getmtime(i) != files_lt[i]: #文件被修改，创建备份            
                delete_file(realname,bdir) #删除多余文件
                shutil(i,bdir+realname+str(time.time())) #复制文件

def delete_file(f,fbase):
    ff=[]
    for root, dirs, files in os.walk(fbase):
        for file in files:
            if f in file:
                file_path = os.path.join(root, file)
                creation_time = os.path.getctime(file_path)
                ff.append((file_path, creation_time))
    ff.sort(key=lambda x: x[1])
    for i in range(CMOST_BACK_FILE-1,len(ff)):
        #删除超过最大备份的文件
        os.unlink(ff[i])

def keyboardListener(k):
    try:
        if k==Key.ctrl and k==Key.p:
            #按下Ctrl+P存档
            #此处存档不占用多余文件
            for i in MANUAL_FILES:
                bdir=os.path.dirname(i)+CDIR
                realname=os.path.basename(i).split(".")[0]
                shutil(i,"#"+bdir+realname+str(time.time())) #复制文件
        t=tkinter.Tk()
        t.geometry("200x100")
        t.overrideredirect(True)
        t.wm_attributes("-alpha",0.5)
        t.wm_attributes("-topmost",True)
        tkinter.Label(t,"保存成功！").pack()
    except:
        pass

def main_keyboard():
    with keyboard.Listener(on_press=keyboardListener) as l:
        l.join()

def main_daemon():
    daemon()

def main():
    for i in FILES: #初始化修改时间
        files_lt[i]=os.path.getmtime(i)
    threading.Thread(target=main_keyboard).start()
    threading.Thread(target=main_daemon).start()
    #双线程并行，start！
    #不过python虽然写的舒服但打包不太方便
    
if __name__=="__main__":
    main()