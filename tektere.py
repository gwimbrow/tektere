#! /usr/bin/env python
import sys,os,ast,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class carto:
  def load(self,dest):
    if 'area' in locals(): del self.area
    stdscr.clear()
    with open('data/'+dest) as choice:
      config=ast.literal_eval(choice.readline())
      script=choice.readlines()
    self.h=len(script)
    self.w=len(max(script,key=len))*2
    self.ypos=(self.h-height)/2
    self.xpos=(self.w-width)/2
    self.area=curses.newpad(self.h+1,self.w+1)
    for l in range(1,len(config)):
      r,g,b=config[l]
      curses.init_color(l,r,g,b)
      curses.init_pair(l,l,l)
    for n in range(0,len(script)):
      x=0
      for b in list(script[n].rstrip()):
        self.area.chgat(n,x,2,curses.color_pair(int(b)))
        x+=2
    stdscr.refresh()
m = carto()
def main(stdscr):
  os.system('setterm -cursor off')
  m.load('origin')
  while True:
    m.area.refresh(m.ypos,m.xpos,max(0,(height-m.h)/2),max(0,(width-m.w)/2),min(height-1,(height+m.h)/2),min(width-1,(width+m.w)/2))
    k=m.area.getch()
    if k==ord('q'): break
    elif k==ord('s') and m.ypos+height<m.h: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('d') and m.xpos+width<m.w: m.xpos+=1
    elif k==ord('a') and 0<m.xpos: m.xpos-=1
  os.system('setterm -cursor on')
curses.wrapper(main)