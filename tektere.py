#! /usr/bin/env python
import sys,os,ast,curses
os.system('setfont '+sys.argv[1]+'.psf')
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class carto:
  def __init__(self): self.fc=0
  def load(self,source):
    with open(source) as choice: self.script=choice.readlines()
    rate,self.h,self.w=ast.literal_eval(self.script[0])
    self.area=curses.newpad(self.h+1,self.w+1)
    self.area.timeout(rate)
    self.keyframes=[]
    for f in range(len(self.script)-1):
      if self.script[f].startswith('#'): self.keyframes.append(f+1)
  def update(self):
    for i in range(self.keyframes[self.fc],self.keyframes[self.fc]+self.h):
      self.area.addstr(i-self.keyframes[self.fc],0,self.script[i],curses.color_pair(1))
    if self.fc<len(self.keyframes)-1: self.fc+=1
    else: self.fc=0
    self.area.refresh((self.h-height)/2,(self.w-width)/2,max(0,(height-self.h)/2),max(0,(width-self.w)/2),min(height,(height+self.h)/2)-1,min(width,(width+self.w)/2)-1)
m = carto()
def main(stdscr):
  curses.init_color(1,1000,1000,1000)
  curses.init_pair(1,1,0)
  curses.curs_set(0)
  m.load(sys.argv[1])
  while True:
    m.update()
    k=m.area.getch()
    if k==ord('q'): break
  curses.curs_set(1)
curses.wrapper(main)