import pyautogui
import random
from pynput import mouse
import math

screenwidth,screenheight=pyautogui.size()

state=0
frame=None
count=0
frame_speed=0.01
state_speed=1

x,y=900,0
px,py=0,0
sizex,sizey=0,0
spdx,spdy=0,0
falling=True
grv=0.0098
frc=0.005
jumppow=1.5

mbleft,mbright=False,False
mboffsetx,mboffsety=0,0

fallid=0

def start():
    global state,count,jumppow,fallid
    state=0
    count=0
    if len(states[get_state("jump")])<5: jumppow=1.5
    else: jumppow=states[state][4]
    fallid=get_state("fall")

def nextstate(states,link,changetorandom=True,default=0):
    global state,count
    base=0
    for l in range(len(link)): #links
        if link[l][0]==state:
            if len(link[l])==2:
                return link[l][1]
            else:
                base+=link[l][2]
    if base!=0: #random multilinks
        rand=random.randint(1, base)
        count=0
        for l in range(len(link)):
            count+=link[l][2]
            if count>=rand:
                return link[l][1]
            
    if not changetorandom:
        count=0
        return default

    base=0  #random next state
    for s in states:
        base+=s[2]
    rand=random.randint(1, base)
    count=0
    for s in range(len(states)):
        count+=states[s][2]
        if count>=rand:
            return s


def setup(x_window,x_char,x_states,x_link,x_frames,x_sizex,x_sizey,x_text_bubble,x_bubble_offset_x,x_bubble_offset_y):
    global window,char,states,link,frames,sizex,sizey,text_bubble,bubble_offset_x,bubble_offset_y
    window,char,states,link,frames,sizex,sizey,text_bubble,bubble_offset_x,bubble_offset_y=x_window,x_char,x_states,x_link,x_frames,x_sizex,x_sizey,x_text_bubble,x_bubble_offset_x,x_bubble_offset_y

def update():
    global state,frame,count,frame_speed,screenwidth,screenheight,x,y,spdx,spdy,grv,frc,px,py,state_speed,window,char,states,link,frames,sizex,sizey,text_bubble,bubble_offset_x,bubble_offset_y,mboffsetx,mboffsety,falling,fallid

    mousex,mousey=pyautogui.position()

    #animation
    count+=frame_speed*state_speed
    if count>states[state][1]:
        state=nextstate(states,link,not falling,fallid)
        if len(states[state])==3:
            state_speed=1
        else:
            state_speed=states[state][3]
        count=0

    #frc
    spdx-=sign(spdx)*min(frc,abs(spdx))
    #grv
    if falling:
        if spdy>0:
            set_state("fall",state)
        spdy+=grv

    #walk
    if states[state][0]=="walk_right":
        if len(states[state])<5: spdx=0.03
        else: spdx=states[state][4]/100
        if x>=screenwidth-sizex:
            set_state("walk_left")
    elif states[state][0]=="walk_left":
        if len(states[state])<5: spdx=-0.03
        else: spdx=-states[state][4]/100
        if x<=0:
            set_state("walk_right")
    #jump
    elif states[state][0]=="jump":
        if count==0:
            spdy=-jumppow
            falling=True
    #dash
    elif states[state][0]=="dash_right":
        if count==0:
            angle=random.randrange(0.2617,1.3089)
            if len(states[state])<5:
                spdx=jumppow*math.cos(angle)
                spdy=-jumppow*math.sin(angle)
            else:
                spdx=states[state][4]*math.cos(angle)
                spdy=-states[state][4]*math.sin(angle)
        if x>=screenwidth-sizex:
            set_state("dash_left")
    elif states[state][0]=="dash_left":
        if count==0:
            angle=random.randrange(0.2617,1.3089)
            if len(states[state])<5:
                spdx=-jumppow*math.cos(angle)
                spdy=-jumppow*math.sin(angle)
            else:
                spdx=-states[state][4]*math.cos(angle)
                spdy=-states[state][4]*math.sin(angle)
        if x>=screenwidth-sizex:
            set_state("dash_right")
    #grabbed
    elif states[state][0]=="grabbed":
        if not mbleft:
            falling=True
            set_state("fall")
    #custom ["name",duration,prob,speed,mx,my,"options",Mx,My]  c-constant,j-jump,l-lerp ; rd-rand dir ; rr-rand range
    elif states[state][0]!="fall" and states[state][0]!="idle":
        minx,miny=0,0
        mx,my=0,0 #0-const 1-jump 2-lerp
        rdx,rdy=False,False
        rrx,rry=False,False
        maxx,maxy=0,0

        sx,sy=1,1
        if len(states[state])>=7:
            options=states[state][6]
            if ("jx" in options):
                mx=1
            elif ("lx" in options):
                mx=2
            if ("jy" in options):
                my=1
            elif ("ly" in options):
                my=2
            rdx,rdy=("rdx" in options),("rdy" in options)
            rrx,rry=("rrx" in options),("rry" in options)
        if len(states[state])>=5: minx=states[state][4]
        if len(states[state])>=6: miny=states[state][5]
        nxsp,nysp=minx,miny
        if len(states[state])>=8: maxx=states[state][7]
        if len(states[state])>=9: maxy=states[state][8]

        if count==0:
            if rrx: nxsp=random.randrange(minx,maxx)
            if rdx:
                if random.randrange(0,1)<0.5: sx=-1
            if rry: nysp=random.randrange(miny,maxy)
            if rdy:
                if random.randrange(0,1)<0.5: sy=-1

        if mx==0: #constant
            spdx=nxsp*sx
        elif mx==1: #jump
            if count==0:
                spdx=nxsp*sx
        elif mx==2: #lerp
            spdx=lerp(minx,maxx,count/states[state][1])*sx
        if my==0: #constant
            spdy=-nysp*sy
        elif my==1: #jump
            if count==0:
                spdy=-nysp*sy
                falling=True
        elif my==2: #lerp
            spdy=-lerp(miny,maxy,count/states[state][1])*sy
        #end
        if count+frame_speed*state_speed>states[state][1]:
            falling=True

    #touch ground
    if falling==True:
        if y+sizey+spdx>screenheight:
            y=screenheight-sizey
            spdy=0
            count=0
            set_state("idle")
            falling=False

    #grab
    if mbleft:
        spdx=mousex+mboffsetx-x
        spdy=mousey+mboffsety-y
        set_state("grabbed",state)
        falling=True

    #jumpback
    if x>=screenwidth-sizex and spdx>0:
        spdx*=-1
    elif x<=0 and spdx<0:
        spdx*=-1
    #out bounders
    if x>=screenwidth-sizex+100 or x<=-100:
        set_state("fall")
        falling=True
        x=screenwidth/2-sizex/2
        y=-sizey
        spdx,spdy=0,0

    px,py=x,y
    #apply
    x+=spdx
    y+=spdy
    #window.geometry(f'{sizex}x{sizey}+{int(x)}+{int(y)}')
    frame=frames[state][int(count)]
    char.configure(image=frame)
    char.place(x=x, y=y)
    if text_bubble.cget("text")!="":
        text_bubble.place(x=x+bubble_offset_x, y=y+bubble_offset_y)
    else:
        text_bubble.place(x=screenwidth+30,y=screenheight+30)
    #loop
    window.after(1,update)


def sign(x):
    if x>0: return 1
    elif x<0: return -1
    else: return 0
def lerp(a,b,c):
    return a*(1-c)+b*c

def on_click(mbx, mby, button, pressed):
    global mbleft,mbright,sizex,sizey,mboffsetx,mboffsety
    if mbx>x and mby>y and mbx<x+sizex and mby<y+sizey:
        if button == mouse.Button.left:
            if pressed:
                mbleft=True
                mboffsetx,mboffsety=x-mbx,y-mby
            else: mbleft=False
        else:
            if pressed: mbright=True
            else: mbright=False
    else:
        mbleft,mbright=False,False
listener = mouse.Listener(on_click=on_click)
listener.start()

def get_state(name, default=0):
    statefind=default
    for i in range(len(states)):
        if states[i][0]==name:
            return i
    print("no state",name)
    return statefind
def set_state(name, default=0):
    global state_speed,state,count
    state=get_state(name,default)
    if len(states[state])==3:
        state_speed=1
    else:
        state_speed=states[state][3]
    #prevent lenght distance crash
    if count>states[state][1]:
        count=0
    return state