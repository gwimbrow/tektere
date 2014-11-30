#! /usr/bin/env python
import curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class carto:
  def __init__(self): self.fc=0
  def load(self):
    with open('source') as choice: self.script=choice.readlines()
    rate=int(self.script[0])
    self.frames=[self.script.index(f) for f in self.script if f.startswith('#')]
    self.h=len(self.script[self.frames[0]+1:self.frames[1]])
    self.w=len(max(self.script,key=len))-1
    self.ypos=(self.h-height)/2
    self.xpos=(self.w-width)/2
    self.area=curses.newpad(self.h+1,self.w+1)
    self.area.timeout(rate)
  def update(self):
   frame=self.script[self.frames[self.fc]+1:self.frames[self.fc+1]]
   if self.fc<len(self.frames)-2: self.fc+=1
   else: self.fc=0
   for y in range(len(frame)):
     x=0
     for j in list(frame[y].rstrip()):
       if j!=' ': self.area.addstr(y,x,j)
       x+=1
   self.area.refresh(self.ypos,self.xpos,max(0,(height-self.h)/2),max(0,(width-self.w)/2),min(height,(height+self.h)/2)-1,min(width,(width+self.w)/2)-1)
m = carto()
def main(stdscr):
  curses.curs_set(0)
  m.load()
  while True:
    stdscr.clear()
    m.update()
    k=m.area.getch()
    if k==ord('q'): break
    elif k==ord('s') and m.ypos+height<m.h: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('d') and m.xpos+width<m.w: m.xpos+=1
    elif k==ord('a') and 0<m.xpos: m.xpos-=1
  curses.curs_set(1)
curses.wrapper(main)
