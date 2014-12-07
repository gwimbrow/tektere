#! /usr/bin/env python
import sys,os,ast,curses
os.system('setfont '+sys.argv[1]+'.psf')
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class carto:
  def __init__(self): self.fc=0
  def load(self):
    with open(sys.argv[1]) as choice:
      self.config=ast.literal_eval(choice.readline())
      self.script=choice.readlines()
    self.rate,self.h,self.w=self.config[0]
    for c in range(1,3):
      r,g,b=self.config[c]
      curses.init_color(c,r,g,b)
      curses.init_pair(c,c-1,c)
    self.area=curses.newpad(self.h+1,self.w+1)
    self.area.timeout(self.rate)
    self.keyframes=[]
    for f in range(len(self.script)-1):
      if self.script[f].startswith('#'): self.keyframes.append(f+1)
  def update(self):
    for i in range(self.keyframes[self.fc],self.keyframes[self.fc]+self.h):
      line=list(self.script[i])
      for l in range(len(line)-1):
        for group in [map(str,g) for g in self.config[3:] if line[l] in map(str,g)]:
          self.area.addstr(i-self.keyframes[self.fc],l,line[l],curses.color_pair(2))
          if group.index(line[l])<len(group)-1: n=group[group.index(line[l])+1]
          else: n=group[0]
          line[l]=n
      self.script[i]=''.join(line)
    if self.fc<len(self.keyframes)-1: self.fc+=1
    else: self.fc=0
    self.area.refresh((self.h-height)/2,(self.w-width)/2,max(0,(height-self.h)/2),max(0,(width-self.w)/2),min(height,(height+self.h)/2)-1,min(width,(width+self.w)/2)-1)
m = carto()
def main(stdscr):
  curses.curs_set(0)
  m.load()
  while True:
    m.update()
    k=m.area.getch()
    if k==ord('q'): break
  curses.curs_set(1)
curses.wrapper(main)