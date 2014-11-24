#! /usr/bin/env python
import ast,math,curses
stdscr=curses.initscr()
stdscr.nodelay(1)
stdscr.idlok(1)
height,width=stdscr.getmaxyx()
class carto:
  def __init__(self): self.fc=0
  def load(self):
    with open('source') as choice:
      config=ast.literal_eval(choice.readline())
      self.script=choice.readlines()
    self.rate,self.duration=config[0]
    for j in range(1,len(config)):
      r,g,b=config[j]
      curses.init_color(j,r,g,b)
      curses.init_pair(j,j,j)
  def rect(self,t,r,b,l,c):
    for y in range(max(0,int(t)),min(height,int(height-b))):
      for x in range(max(0,int(l)),min(width,int(width-r))):
        stdscr.chgat(y,x,1,curses.color_pair(c))
  def update(self):
    stdscr.erase()
    for i in self.script:
      if i.startswith('rect'): exec('self.'+i)
    stdscr.refresh()
    if self.fc<self.duration: self.fc+=1
    else: self.fc=0
m = carto()
def main(stdscr):
  curses.curs_set(0)
  m.load()
  while True:
    curses.napms(m.rate)
    m.update()
    k=stdscr.getch()
    if k==ord('q'): break
  curses.curs_set(1)
curses.wrapper(main)