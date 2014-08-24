#! /usr/bin/env python
import os,re,curses
from subprocess import call
from ast import literal_eval
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    with open('log') as log: self.cells=literal_eval(log.read())
    self.diagrams=['0.0','0.1','0.2','1.2','2.2','2.1','2.0','1.0']
  def load(self,cell):
    if 'textarea' in locals(): del self.textarea
    stdscr.clear()
    self.cell=cell
    if self.cell=='1.1': call(['nano','-t','/'.join(['data',self.cells[self.cell]])])
    os.system('setterm -cursor off')
    with open('/'.join(['data',self.cells[self.cell]])) as choice: script=choice.readlines()
    self.h=len(script)
    self.w=len(max(script,key=len))
    self.textarea=curses.newpad(self.h,self.w)
    self.textarea.bkgd(' ',curses.color_pair(1))
    self.ypos=0
    self.xpos=0
    count=0
    y=0
    for s in script:
      x=0
      for w in re.split('(\s+)',s.rstrip()):
        if self.cell=='1.1' and w in [f for f in os.listdir('data')] and count<len(self.diagrams):
          self.cells[self.diagrams[count]]=w
          count+=1
        self.textarea.addstr(y,x,w)
        x+=len(w)
      y+=1
    cy,cx=map(int,self.cell.split('.'))
    self.adjacents=['.'.join(map(str,[cy-1,cx])),'.'.join(map(str,[cy,cx+1])),'.'.join(map(str,[cy+1,cx])),'.'.join(map(str,[cy,cx-1]))]
    for adj in [a for a in self.adjacents if a in self.cells.keys()]:
      y,x={0:(0,2),1:(1,4),2:(2,2),3:(1,0)}[self.adjacents.index(adj)]
      stdscr.addch(y,x,curses.ACS_DIAMOND)
    stdscr.addstr(height-1,width-89,'w: up / a: left / s: down / d: right / i: north / j: west/ k: south / l: east / q: quit')
    stdscr.refresh()
m = message()
def main(stdscr):
  curses.init_color(1,1000,1000,1000)
  curses.init_pair(1,1,0) # base
  curses.init_color(2,0,0,1000)
  curses.init_pair(2,2,0) # interface
  stdscr.bkgd(' ',curses.color_pair(2))
  kc=[ord('i'),ord('l'),ord('k'),ord('j')]
  m.load('1.1')
  while True:
    m.textarea.refresh(m.ypos,m.xpos,max(3,(height/2)-(m.h/2)),max(0,(width/2)-(m.w/2)),min(height-3,(height/2)+(m.h/2)),min(width-1,(width/2)+(m.w/2)))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('d') and m.xpos+width<m.w: m.xpos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('a') and 0<m.xpos: m.xpos-=1
    elif k in kc and m.adjacents[kc.index(k)] in m.cells.keys(): m.load(m.adjacents[kc.index(k)])
  with open('log','w') as log: log.write(str(m.cells))
  os.system('setterm -cursor on')
curses.wrapper(main)