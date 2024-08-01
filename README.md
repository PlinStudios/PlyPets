# PlyPets

This a deskstop pet engine i made just for fun based on this [article](https://medium.com/analytics-vidhya/create-your-own-desktop-pet-with-python-5b369be18868) but highly changed(it was so messy but with all the features this one became worse), also it can connect to CharacterAI so you can talk with your pets

Featuring a stickman and Rikka Takanashi from chuunibyou

## Installation

Download the source and save it somewhere

You need to have [Python](https://www.python.org) installed
And also theres some libraries you should install

Paste this in your teminal
```bash
pip install git+https://github.com/kramcat/CharacterAI.git
pip install pyautogui
pip install pynput
pip install AppOpener
```

## Running

Run pet.py with visual studio or the terminal, open powershell on your folder and type
```bash
python pet.py
```
NOTE: Opening with python(.exe) doesn't seem to work so use the terminal

Now you can play with your pet

Right click on it and you will see the option to:
TALK: input a text and the pet will respond
Configuration: here you can change pet and setup your CharacterAI account and the weather api
EXIT: closes the program

## Making Pets

What all have been waiting for…
In the folder pets create a new folder named as your character, there you will put gifs of the character actions, and leave there a file named charcfg.ply where you have to put in separate lines:
1 - A list of the states, each state use this format ["name",frames,probability,speed], write the name the same as the gif but without the format, and also you can use an extra parameter for built-in actions, for example the movement speed for "walk_left"
2 - A list of list pairing an action and the one that Will follow, this is usefull for transitions, also if you use a third parameter this Will be use as the probability of that one being selectet something like this [["idle_to_sleep","sleep"],["jump","kick",1],["jump","fall",5]]
3 - Width
4 - Height
5 - CharacterAI character id, can be found on the link of the chat, if you don't want to use it write None
6 - Default Response - shown when character ai is unactive or teres no conection
7 - Message Time - the time a message of 10 characters will be shown, it scales depending on the lenght
8 - Message X Offset
9 - Message Y Offset
10 - Background Color - this is the color that will be used as transparent so set it to a color your animation doesn't use

NOTE: Probabilities are based on the sum of probabilities, not percentage, but they can be used as percentage anyway
CUSTOM STATES: if you want your custom state to move, first it doesn't have to be the ones especified the code:
```python
"idle","walk_right","walk_left","jump","dash_left","dash_right","grabbed","fall"
```
now you put these parameters at the end: x1,y2,cfg,x2,y2
if cfg you write the type of movement with the axis, you can combine
here some examples:
cx - constant movement in the x with speed x1
jy - jump in the y with ini speed x1
lx - lerp speed in the x from x1 to x2

rrx - x1 is changed to a random float between x1 and x2
rdy - select a random direction for movement in y

Here i'll leave an example of a charcfg.ply
```python
[["idle",2,8,0.25],["walk_left",4,4,0.5,3],["walk_right",4,4,0.5,3],["grabbed",4,0,0.5],["jump",2,2,0.30],["fall",2,0,2],["fly",5,2,3,0,0,"ly",0,1]]
[["fly","fall",3],["fly","fly",1]]
100
100
MgMnZKsbnovx1ve17WxieDjWnhksZ1UBapjoCRloTnY
hello
2
80
0
blue
```

Anyways you can make the file while you test it, go to configuration click sabe and the file will be reloaded

## Do whatever

If you want to make changes to the program do it, you can change petbehav.py update function to change what the pet does, but if you want to publish it just credit me
