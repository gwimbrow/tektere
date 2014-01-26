#! /usr/bin/env python
import sys, os, curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class room:
  def __init__(self):
    self.firstrun=True
    self.dirs = []
    for names in os.listdir(sys.path[0]+'/data'): self.dirs.append(names.lower())
    self.reset()
  def reset(self):
    self.ypos,self.xpos=0,0
    self.links=[]
    self.selection=[]
    self.count=0
    stdscr.clear()
    stdscr.refresh()
  def load(self,sub):
    with open('log') as log: present=int(log.read().split(':')[1].rstrip())
    if self.firstrun==True:
      timestamp=str(present)
      self.firstrun = False
    else:
      del self.textarea
      self.reset()
      files=[]
      for names in os.listdir(sys.path[0]+'/data/'+sub): files.append(int(names))
      if present<max(files):
        files.sort()
        for f in files:
          if f>present:
            timestamp=f
            break
      else: timestamp=max(files)
    script=[]
    with open(sys.path[0]+'/data/'+sub+'/'+str(timestamp)) as choice: script=choice.readlines()
    th=len(script)+6
    tw=len(max(script,key=len))+6
    self.textarea=curses.newpad(th,tw)
    self.textarea.bkgd(' ',curses.color_pair(3))
    y,x=2,3
    for i in range(len(script)):
      if script[i].startswith('{'):
        quote = script[i].rstrip()[1:-1].split(':')
        with open(sys.path[0]+'/data/'+quote[0]+'/'+quote[1]) as quoted:
          lines = quoted.readlines()
          self.textarea.resize(max(th,th+len(lines)-1),max(tw,len(max(lines,key=len))))
          self.textarea.addstr(y,x,quote[0]+':',curses.color_pair(4))
          y+=1
          for l in lines:
            self.textarea.addstr(y,x,l,curses.color_pair(4))
            y+=1
      else:
        words=script[i].rstrip().split(' ')
        for w in words:
          if w.lower() in self.dirs:
            self.textarea.addstr(y,x,w,curses.color_pair(1))
            self.links.append([y,x,w.lower()])
          else: self.textarea.addstr(y,x,w)
          x+=len(w)+1
        y+=1
        x=3
    self.textarea.addstr(th-2,tw-len(str(timestamp))-2,str(timestamp))
    with open('log','w') as log: log.write(sub+':'+str(timestamp))
  def navigate(self):
    self.textarea.chgat(self.links[self.count][0],self.links[self.count][1],len(self.links[self.count][2]),curses.color_pair(2))
    if self.selection!=[]: self.textarea.chgat(self.selection[0],self.selection[1],len(self.selection[2]),curses.color_pair(1))
    self.selection=self.links[self.count]
    if self.count<len(self.links)-1: self.count+=1
    else: self.count=0
    return self.selection[2]
r = room()
def main(stdscr):
  global height,width
  curses.init_color(1,325,486,627)
  curses.init_color(2,114,122,129)
  curses.init_color(3,216,231,255)
  curses.init_pair(1,1,2)
  curses.init_pair(2,2,1)
  curses.init_pair(3,curses.COLOR_WHITE,2)
  curses.init_pair(4,3,2)
  curses.curs_set(0)
  with open('log') as log: r.load(log.read().split(':')[0])
  target=''
  while True:
    r.textarea.refresh(r.ypos,r.xpos,max(0,(height/2)-(r.textarea.getmaxyx()[0]/2)),max(0,(width/2)-(r.textarea.getmaxyx()[1]/2)),min(height-1,(height/2)+(r.textarea.getmaxyx()[0]/2)),min(width-1,(width/2)+(r.textarea.getmaxyx()[1]/2)))
    k=r.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t'): target=r.navigate()
    elif k==ord('e') and target!='':
      r.load(target)
      target=''
    elif k==ord('s') and r.ypos+height<r.textarea.getmaxyx()[0]: r.ypos+=1
    elif k==ord('w') and 0<r.ypos: r.ypos-=1
    elif k==ord('d') and r.xpos+width<r.textarea.getmaxyx()[1]: r.xpos+=1
    elif k==ord('a') and 0<r.xpos: r.xpos-=1
  stdscr.clear()
  stdscr.refresh()
  curses.curs_set(1)
curses.wrapper(main)