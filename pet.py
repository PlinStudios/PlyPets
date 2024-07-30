import tkinter as tk
from tkinter import ttk
import json
import petbehav
import os
import chat
from tkinter import simpledialog
import threading
import asyncio

def strtobool(x):
    return x=="True"
#list option
langslist=["...","ES","EN"]
f=open("_utils_/cfg.ply","r")
myfile=f.read().splitlines()
pet=myfile[0]
lang=myfile[1]
usecai=strtobool(myfile[2])
cai_token=myfile[3]
usetime=strtobool(myfile[4])
useweather=strtobool(myfile[5])
weathertoken=myfile[6]
lat=float(myfile[7])
lon=float(myfile[8])
usecommand=strtobool(myfile[9])
userequest=strtobool(myfile[10])
f.close()
petlist=["..."]+[ f.name for f in os.scandir("pets") if f.is_dir() and f.name[0]!="_" ]

#create window
window = tk.Tk()

#get character
states=[]
link=[]
defaultdialog="hello!"
char_token=""
frames=[]
sizex,sizey=100,100
messagetime=1
bubble_offset_x,bubble_offset_y=100,0
pettranscol="black"
def getchardata(charname):
    global states,link,defaultdialog,char_token,frames,sizex,sizey,messagetime,bubble_offset_x,bubble_offset_y,pettranscol
    f=open(f"pets/{charname}/charcfg.ply","r")
    myfile=f.read().splitlines()
    #get states and anim links
    states=json.loads(myfile[0]) #[[name,lenght,probability,speed],...] if speed defaults to 1
    if len(myfile)>1: link=json.loads(myfile[1]) #connections from an state to other, used for multistate animations  [start,end,prob] if prob does not exist select automatically
    else: link=[]
    if len(myfile)>3:
        sizex=int(myfile[2])
        sizey=int(myfile[3])
    else: sizex,sizey=100,100
    if len(myfile)>4: char_token=myfile[4]
    else: char_token="None"
    if len(myfile)>5: defaultdialog=myfile[5]
    else: defaultdialog="hello!"
    if len(myfile)>6: messagetime=int(myfile[6])
    else: messagetime=1
    if len(myfile)>8:
        bubble_offset_x=int(myfile[7])
        bubble_offset_y=int(myfile[8])
    else: bubble_offset_x,bubble_offset_y=100,0
    if len(myfile)>9: pettranscol=myfile[9]
    else: pettranscol="black"
    f.close()

    #get frames
    frames=[]
    for fr in range(len(states)):
        frames.append([tk.PhotoImage(file=f"pets/{charname}/{states[fr][0]}.gif",format = 'gif -index %i' %(i)) for i in range(states[fr][1])])

    petbehav.setup(window,char,states,link,frames,sizex,sizey,text_bubble,bubble_offset_x,bubble_offset_y)
    petbehav.start()

    #procces string link
    for i in link:
            if type(i[0])==str: i[0]=petbehav.get_state(i[0])
            if type(i[1])==str: i[1]=petbehav.get_state(i[1])

#set chat
char_ai = chat.CharacterAIChat()
loop = asyncio.get_event_loop()

def setup_ai():
    threading.Thread(target=run_setup).start()

def run_setup():
    loop.run_until_complete(char_ai.setup(cai_token,char_token))

def send_message():
    message = simpledialog.askstring("TALK", "Enter your message:")
    if message:
        threading.Thread(target=run_get_response, args=(message,)).start()

def run_get_response(text):
    response = loop.run_until_complete(char_ai.get_response(text,defaultdialog,usecai))
    #show in bubble
    text_bubble.config(text=response)
    t=threading.Timer(messagetime*len(text)/10, quit_response)
    t.start()

def quit_response():
    text_bubble.config(text="")



#windows configuration
window.overrideredirect(True)
def settransparencycolor(col='black'):
    window.wm_attributes('-transparentcolor',col)
    window.configure(background=col)
    window.config(highlightbackground=col)
    char.configure(bg=col)
window.wm_attributes("-topmost", 1)
window.geometry(f"{petbehav.screenwidth}x{petbehav.screenheight}+0+0")
#window.geometry("1920x1080+0+0")
#char
char = tk.Label(window,bd=0,bg='black')
char.pack()
#text bubble
text_bubble = tk.Label(window, text="", bg='white', fg='black', font=("Arial", 10), wraplength=150, justify='left')
text_bubble.place(x=50, y=50)
#configpanel
def open_config():
    config_window = tk.Toplevel(window)
    config_window.title("Configuration")
    config_window.geometry("200x500")

    # Add configuration options (example)
    tk.Label(config_window, text="PET OPTIONS").pack()
    tk.Label(config_window, text="Pet:").pack()
    petid = tk.StringVar()
    ttk.OptionMenu( config_window , petid , *petlist).pack()
    petid.set(pet)
    tk.Label(config_window, text="lang:").pack()
    langid = tk.StringVar()
    ttk.OptionMenu( config_window , langid , *langslist).pack()
    langid.set(lang)
    tk.Label(config_window, text="AI OPTIONS").pack()
    uiusecai = tk.BooleanVar()
    tk.Checkbutton(config_window, text="Use CharacterAI",variable=uiusecai).pack()
    uiusecai.set(usecai)
    tk.Label(config_window, text="CharAI TOKEN").pack()
    uicaitoken=ttk.Entry(config_window)
    uicaitoken.insert(0,cai_token)
    uicaitoken.pack()
    def get_token():
        mytoken=chat.login()
        uicaitoken.insert(0,mytoken)
    tk.Button(config_window, text="GET TOKEN",command=get_token).pack()
    uiusetime = tk.BooleanVar()
    tk.Checkbutton(config_window, text="use time context",variable=uiusetime).pack()
    uiusetime.set(usetime)
    uiuseweather = tk.BooleanVar()
    tk.Checkbutton(config_window, text="use weather context",variable=uiuseweather).pack()
    uiuseweather.set(useweather)
    tk.Label(config_window, text="OpenWeatherMap Token").pack()
    uiweathertoken=ttk.Entry(config_window)
    uiweathertoken.insert(0,weathertoken)
    uiweathertoken.pack()
    tk.Label(config_window, text="latitude").pack()
    uilat=ttk.Entry(config_window)
    uilat.insert(0,lat)
    uilat.pack()
    tk.Label(config_window, text="longitude").pack()
    uilon=ttk.Entry(config_window)
    uilon.insert(0,lon)
    uilon.pack()
    tk.Label(config_window, text="AI COMMANDS").pack()
    uiusecommand = tk.BooleanVar()
    tk.Checkbutton(config_window, text="use commands",variable=uiusecommand).pack()
    uiusecommand.set(usecommand)
    uiuserequest = tk.BooleanVar()
    tk.Checkbutton(config_window, text="use request",variable=uiuserequest).pack()
    uiuserequest.set(userequest)
    tk.Button(config_window, text="SAVE", command=lambda: save_config(petid.get(),langid.get(),uiusecai.get(),uicaitoken.get(),uiusetime.get(),uiuseweather.get(),uilat.get(),uilon.get(),uiusecommand.get(),uiuserequest.get(),uiweathertoken.get())).pack()
def save_config(s_pet,s_lang,s_usecai,s_caitoken,s_usetime,s_useweather,s_lat,s_lon,s_usecommand,s_userequest,s_weathertoken):
    global pet,lang,usecai,cai_token,usetime,useweather,lat,lon,usecommand,userequest
    pet,lang,usecai,cai_token,usetime,useweather,lat,lon,usecommand,userequest,weathertoken=s_pet,s_lang,s_usecai,s_caitoken,s_usetime,s_useweather,s_lat,s_lon,s_usecommand,s_userequest,s_weathertoken
    cfgfile = open("_utils_/cfg.ply", "w+")
    cfgfile.write(f"{pet}\n{lang}\n{usecai}\n{cai_token}\n{usetime}\n{useweather}\n{weathertoken}\n{lat}\n{lon}\n{usecommand}\n{userequest}")
    cfgfile.close()
    getchardata(pet)
    chat.metadatasetup(pet,usetime,useweather,weathertoken,lon,lat,lang)
    chat.commandsetup(usecommand,userequest)
    settransparencycolor(pettranscol)
    if usecai: setup_ai()

context_menu = tk.Menu(window, tearoff=0)
context_menu.add_command(label="TALK", command=send_message)
context_menu.add_command(label="Configuración", command=open_config)
context_menu.add_command(label="EXIT", command=window.destroy)
def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)
char.bind("<Button-3>", show_context_menu)
#loop the program
getchardata(pet)
chat.metadatasetup(pet,usetime,useweather,weathertoken,lon,lat,lang)
chat.commandsetup(usecommand,userequest)
settransparencycolor(pettranscol)
if usecai: setup_ai()
window.after(1,petbehav.update)
window.mainloop()