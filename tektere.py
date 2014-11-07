#! /usr/bin/env python
import sys,os,ast,curses
stdscr=curses.initscr()
#stdscr.bkgd(curses.ACS_CKBOARD)
height,width=stdscr.getmaxyx()
class carto:
  def __init__(self): self.fc=0
  def load(self):
    if 'area' in locals(): del self.area
    with open('source') as choice:
      config=ast.literal_eval(choice.readline())
      self.script=choice.readlines()
    self.frames=[self.script.index(f) for f in self.script if f.startswith('f')]
    self.h=len(self.script[self.frames[0]+1:self.frames[1]])
    self.w=(len(max(self.script,key=len))-1)*2
    self.ypos=(self.h-height)/2
    self.xpos=(self.w-width)/2
    self.area=curses.newpad(self.h,self.w)
    self.area.nodelay(1)
    for l in range(1,len(config)):
      r,g,b=config[l]
      curses.init_color(l,r,g,b)
      curses.init_pair(l,l,l)
  def update(self):
    frame=self.script[self.frames[self.fc]+1:self.frames[self.fc+1]]
    if self.fc<len(self.frames)-2: self.fc+=1
    else: self.fc=0
    for i in range(len(frame)):
      x=0
      for j in list(frame[i].rstrip()):
        if j!=' ': self.area.chgat(i,x,2,curses.color_pair(int(j)))
        x+=2
    self.area.refresh(self.ypos,self.xpos,max(0,(height-self.h)/2),max(0,(width-self.w)/2),min(height,(height+self.h)/2)-1,min(width,(width+self.w)/2)-1)
m = carto()
def main(stdscr):
  os.system('setterm -cursor off')
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
  os.system('setterm -cursor on')
curses.wrapper(main)