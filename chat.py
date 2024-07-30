from characterai import aiocai, sendCode, authUser

class CharacterAIChat:
    def __init__(self):
        self.cai_token = ""
        self.char_token = ""
        self.client = None
        self.me = None
        self.chat = None
        self.new_chat = None

    async def setup(self, cai_token, char_token):
        self.cai_token = cai_token
        self.char_token = char_token
        self.client = aiocai.Client(self.cai_token)
        self.me = await self.client.get_me()

        self.chat = await self.client.connect()
        self.new_chat, answer = await self.chat.new_chat(self.char_token, self.me.id)

        print(f'{answer.name}: {answer.text}')
        return answer.text

    async def get_response(self, text,defaultdialog,usecai):
        try:
            if usecai and self.char_token!="None": message = await self.chat.send_message(self.char_token, self.new_chat.chat_id, getmetadata()+text)
            print(message.text)
            return textprocess(message.text)
        except:
            return textprocess(defaultdialog)

from tkinter import simpledialog
def login():
    email = simpledialog.askstring("LOGIN step1","Input your email:")
    code = sendCode(email)
    link = simpledialog.askstring("LOGIN step2","Input the link in you email:")
    token = authUser(link, email)

    return token

import datetime
now=datetime.datetime.now().astimezone()
from tkinter import *
import requests
import os
weatherparams={"lat":"-36.60664",
            "lon":"-72.10344",
            "units":"metric",
            "appid":"None",
            "lang" :"sp"}
meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
usetime=False
useweather=False
mychar=""
lang=""
wcon={
    "ES":["sp","[[SYSTEM]]: El dia cambio, el ultimo mensaje se envio en "," , hoy es "," la temperatura minima es ","ºC la maxima ","ºC, la humedad","% la velocidad del viento","km/h, el clima esta "," y la temperatura actual es "],
    "EN":["en","[[SYSTEM]]: The day changed, last message was sent on "," , today is "," minimum temperature is ","ºC the maximum ","ºC, the humidity","% wind speed","km/h, the weather is "," and current temperature "]
    }
def metadatasetup(x_mychar,x_usetime,x_useweather,weathertoken,lon,lat,x_lang):
    global mychar,usetime,useweather,lang
    mychar,usetime,useweather=x_mychar,x_usetime,x_useweather
    weatherparams["appid"]=weathertoken
    weatherparams["lat"]=lat
    weatherparams["lon"]=lon
    lang=x_lang
    weatherparams["lang"]=wcon[lang][0]
def getmetadata():
    if not usetime:
        return ""
    md=""
    now=datetime.datetime.now().astimezone()
    try:
        previous=open("_utils_/"+mychar+"metadata","r").read().splitlines() #0dia 1mes 2año 3hora 4minuto 5segundo 6climamain 7climadesc 8temp 9tmin 10tmax 11humidity 12wind
    except:
        previous=[str(now.day),str(now.month),str(now.year),str(now.hour),str(now.minute),str(now.second),"","","","","","",""]

    pdate="["+previous[0]+"/"+previous[1]+"/"+previous[2]+"]"
    date="["+str(now.day)+"/"+str(now.month)+"/"+str(now.year)+"]"
    if date!=pdate:
        if useweather:
            weather=requests.get("http://api.openweathermap.org/data/2.5/weather",params=weatherparams).json()
            md=wcon[lang][1]+pdate+wcon[lang][2]+date+wcon[lang][3]+str(weather["main"]["temp_min"])+wcon[lang][4]+str(weather["main"]["temp_max"])+wcon[lang][5]+str(weather["main"]["humidity"])+wcon[lang][6]+str(weather["wind"]["speed"])+wcon[lang][7]+str(weather["weather"][0]["main"])+","+str(weather["weather"][0]["description"])+wcon[lang][8]+str(weather["main"]["temp"])+"ºC\n"
        else:
            weather={"weather":[{"main":"","description":""}],"main":{"temp":"","temp_min":"","temp_max":"","humidity":""},"wind":{"speed":""}}
            md=wcon[lang][1]+pdate+wcon[lang][2]+date+"\n"
        previous[0]=str(now.day)
        previous[1]=str(now.month)
        previous[2]=str(now.year)
        previous[3]=str(now.hour)
        previous[4]=str(now.minute)
        previous[5]=str(now.second)
        previous[6]=str(weather["weather"][0]["main"])
        previous[7]=str(weather["weather"][0]["description"])
        previous[8]=str(weather["main"]["temp"])
        previous[9]=str(weather["main"]["temp_min"])
        previous[10]=str(weather["main"]["temp_max"])
        previous[11]=str(weather["main"]["humidity"])
        previous[12]=str(weather["wind"]["speed"])
    elif previous[3]!=str(now.hour):
        if useweather:
            weather=requests.get("http://api.openweathermap.org/data/2.5/weather",params=weatherparams).json()
        else:
            weather={"weather":[{"main":"","description":""}],"main":{"temp":"","temp_min":"","temp_max":"","humidity":""},"wind":{"speed":""}}
        md="[[SYSTEM]]: Son las "+str(now.hour)+"hrs, han pasado "+str(now.hour-int(previous[3]))+" horas"
        previous[3]=str(now.hour)
        if useweather:
            if previous[7]!=str(weather["weather"][0]["description"]):
                md+=", el clima actual es "+str(weather["weather"][0]["description"])
                previous[7]=str(weather["weather"][0]["description"])
            if previous[8]!=str(weather["main"]["temp"]):
                md+=", la temperatura actual es de"+str(weather["main"]["temp"])+"ºC"
                previous[8]=str(weather["main"]["temp"])
        md+="\n"
    hour="["+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+"]"
    md+=hour+": "
    previous[4]=str(now.minute)
    previous[5]=str(now.second)
    for i in range(len(previous)):
        previous[i]+="\n"
    open("_utils_/"+mychar+"metadata","w").writelines(previous)
    return md

#COMMAND
command_aviable=["TALK","COPY","OPEN"]
request_aviable=["PASTE","DATE","MONTH","YEAR","HOUR","HOURALONE","MINUTE","SECOND","REQUESTFILE","REQUESTDIRECTORY"]

usecommand,userquest=False,False
def commandsetup(x_usecommand,x_userquest):
    global usecommand,userquest
    usecommand,userquest=x_usecommand,x_userquest
def textprocess(txt):
    messageshown=""
    mode=0 #0 write 1 command 2 request
    start=0
    command=""
    argument=""
    request=""
    for i in range(len(txt)):
        if txt[i]=="[":
            mode=1
            start=i
        elif txt[i]=="{" and mode==0:
            mode=2
            start=i

        #text mode
        if mode==0: messageshown+=txt[i]
        #command mode
        if mode==1 and txt[i]=="]":
            command=txt[start+1:i].upper()
            #check if exists
            if command in command_aviable:
                if command=="TALK": mode=0
                start=i
            elif command in request_aviable:
                request=command
                r=getrequest(request)
                messageshown+=r
                mode=0
        if mode==1 and (i+1==len(txt) or txt[i+1]=="["):
            ogargument=txt[start+1:i+1]
            argument=textprocess(ogargument)
            c=execcomand(command,argument)
            messageshown+=c
        #request mode
        if mode==2 and txt[i]=="}":
            request=txt[start+1:i].upper()
            #check if exists
            if request in request_aviable:
                r=getrequest(request)
                #errorcheck
                messageshown+=r
                mode=0
            elif request in command_aviable:
                command=request
                command=txt[start+1:i]
                if command=="TALK": mode=0
                else: mode=1
                start=i


    return messageshown

import time
import pyperclip as clipboard
import datetime
import tkinter as tk
from tkinter  import filedialog as fd
import AppOpener
import subprocess
import os
import json
import webbrowser
try:
    extraapps=json.loads(open("_utils_/"+"extraprograms","r").read())
except:
    open("_utils_/"+"extraprograms","w").write("{"+"}")
    extraapps={}

def execcomand(command,argument):
    if not usecommand:
        print("not using command")
        return 0
    if command=="COPY":
        clipboard.copy(argument)
    elif command=="OPEN" or command=="RUN":
        try:
            AppOpener.open(argument, match_closest=True, throw_error=True)
        except:
            argument=argument.lower().replace(" ","")
            if argument in extraapps:
                print(argument,extraapps[argument])
                subprocess.Popen(extraapps[argument], cwd=os.path.dirname(extraapps[argument]))
                time.sleep(5)
            else:
                location=fd.askopenfilename(title=argument, initialdir=os.getcwd())
                if location!=None:
                    extraapps.update({argument: location})
                    subprocess.Popen(location, cwd=os.path.dirname(location))
                    open("_utils_/"+"extraprograms","w").writelines(json.dumps(extraapps))
                    time.sleep(5)
    elif command=="SEARCH":
        webbrowser.open(f'https://www.google.com/search?q={argument.replace(" ","+")}')
    elif command=="SEARCHIMG":
        webbrowser.open(f'https://www.google.com/search?q={argument.replace(" ","+")}&udm=2&fbs')
    elif command=="SEARCHYT" or command=="SEARCHYOUTUBE":
        webbrowser.open(f'https://www.youtube.com/results?search_query={argument.replace(" ","+")}')
    else: #dont recognize command so just print the text
        return argument


    return ""


def getrequest(request):
    if not userquest:
        print("not using request")
        return ""
    result=""
    if request=="PASTE":
        result=clipboard.paste()
    elif request=="DATE":
        now=datetime.datetime.now().astimezone()
        result=str(now.day)+"/"+meses[now.month]+"/"+str(now.year)
    elif request=="DAY":
        now=datetime.datetime.now().astimezone()
        result=str(now.day)
    elif request=="MONTH":
        now=datetime.datetime.now().astimezone()
        result=meses[now.month]
    elif request=="YEAR":
        now=datetime.datetime.now().astimezone()
        result=str(now.year)
    elif request=="HOUR":
        now=datetime.datetime.now().astimezone()
        result=str(now.hour)+":"+str(now.minute)+":"+str(now.second)
    elif request=="HOURALONE":
        now=datetime.datetime.now().astimezone()
        result=str(now.hour)
    elif request=="MINUTE":
        now=datetime.datetime.now().astimezone()
        result=str(now.minute)
    elif request=="SECOND":
        now=datetime.datetime.now().astimezone()
        result=str(now.second)
    elif request=="REQUESTFILE":
        result=fd.askopenfilename()
    elif request=="REQUESTDIRECTORY":
        result=fd.askdirectory()

    return result