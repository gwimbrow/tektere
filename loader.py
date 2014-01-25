#! /usr/bin/env python
import sys, os, curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
firstrun=True
class room:
  def __init__(self):
    self.storyhash={}
    with open('log') as log: pairs=log.readlines()[1].split(',')
    for p in pairs:
      key,value=p.split(':')[0],p.split(':')[1]
      self.storyhash[key]=int(value)
    self.reset()
  def reset(self):
    self.ypos,self.xpos=0,0
    self.current_specials=[]
    self.current_selection=[]
    self.current_visible=[]
    self.count=0
  def open_room(self,sub):
    global firstrun
    if firstrun==False:
      del self.textarea
      self.reset()
    script=[]
    with open(sys.path[0]+'/data/'+sub+'/'+str(self.storyhash[sub])) as choice: script=choice.readlines()
    th=len(script)
    tw=len(max(script,key=len))
    self.textarea=curses.newpad(th+1,tw+1)
    y,x=0,0
    for i in range(len(script)):
      words=script[i].rstrip().split(' ')
      for w in words:
        if w.lower() in self.storyhash.keys():
          self.textarea.addstr(y,x,w,curses.color_pair(1))
          self.current_specials.append([y,x,w])
        else: self.textarea.addstr(y,x,w)
        x+=len(w)+1
      y+=1
      x=0
    files=[]
    for names in os.listdir(sys.path[0]+'/data/'+sub):
      files.append(int(names))
    if self.storyhash[sub]!=max(files):
      files.sort()
      self.storyhash[sub]=files[files.index(self.storyhash[sub])+1]
    with open('log','w') as log: 
      storystring = []
      for n in range(len(self.storyhash.keys())): storystring.append(self.storyhash.keys()[n]+':'+str(self.storyhash.values()[n]))
      log.write(sub.lower()+'\n'+','.join(storystring))
    if firstrun==True: firstrun=False
  def nextspecial(self):
    global height,width
    visible=[]
    for j in self.current_specials:
      if self.ypos-1<j[0]<self.ypos+height and self.xpos-1<j[1]<self.xpos+width: visible.append(j)
    if len(visible)!=0:
      if self.current_visible!=visible: self.count = 0
      self.textarea.chgat(visible[self.count][0],visible[self.count][1],len(visible[self.count][2]),curses.color_pair(2))
      if self.current_selection!=[]: 
        self.textarea.chgat(self.current_selection[0],self.current_selection[1],len(self.current_selection[2]),curses.color_pair(1))
      self.current_visible=visible
      self.current_selection=visible[self.count]
      if self.count<len(visible)-1: self.count+=1
      else: self.count = 0
      return self.current_selection[2]
    else: return ''
r = room()
def main(stdscr):
  global height,width
  curses.curs_set(0)
  curses.init_color(1,600,140,80)
  curses.init_color(2,1000,0,0)
  curses.init_pair(1,1,curses.COLOR_BLACK);
  curses.init_pair(2,2,curses.COLOR_BLACK);
  with open('log') as log: r.open_room(log.readlines()[0].rstrip())
  lock=''
  while True:
    r.textarea.refresh(r.ypos,r.xpos,max(0,(height/2)-(r.textarea.getmaxyx()[0]/2)),max(0,(width/2)-(r.textarea.getmaxyx()[1]/2)),min(height-1,(height/2)+(r.textarea.getmaxyx()[0]/2)),min(width-1,(width/2)+(r.textarea.getmaxyx()[1]/2)))
    k=r.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t'): lock=r.nextspecial()
    elif k==ord('e') and lock!='': r.open_room(lock)
    elif k==ord('s') and r.ypos+height<r.textarea.getmaxyx()[0]: r.ypos+=1
    elif k==ord('w') and 0<r.ypos: r.ypos-=1
    elif k==ord('d') and r.xpos+width<r.textarea.getmaxyx()[1]: r.xpos+=1
    elif k==ord('a') and 0<r.xpos: r.xpos-=1
  stdscr.clear()
  stdscr.refresh()
  curses.curs_set(1)
curses.wrapper(main)