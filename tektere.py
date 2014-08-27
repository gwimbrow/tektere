#! /usr/bin/env python
import os,re,curses
from ast import literal_eval
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    self.cardinals=['0.1','1.2','2.1','1.0']
    self.config={}
    for f in os.listdir('data'):
      with open('/'.join(['data',f])) as file: self.config[f]=literal_eval(file.readline().rstrip())
  def load(self,cell):
    self.cell=cell
    self.ypos=0
    self.xpos=0
    self.count=0
    if 'textarea' in locals(): del self.textarea
    stdscr.clear()
    if self.cell=='1.1':
      self.links={}
      self.selected=()
      self.diacount=0
      self.cells={'1.1':''}
      script=self.config.keys()
    else:
      with open('/'.join(['data',self.cells[self.cell]])) as choice: script=choice.readlines()[1:]
    self.h=len(script)
    self.w=len(max(script,key=len))
    self.textarea=curses.newpad(self.h,self.w)
    y=0
    for s in script:
      x=0
      for w in re.split('(\s+)',s.rstrip()):
        if self.cell=='1.1':
          self.links[self.count]=(y,x,w,curses.color_pair(1))
          self.count+=1
        self.textarea.addstr(y,x,w,curses.color_pair(1))
        x+=len(w)
      y+=1
    self.count=0
    self.drawinterface()
  def drawinterface(self):
    if self.cell!='1.1':
      for num,val in self.links.iteritems():
        if val[2]==self.cells[self.cell]: stdscr.addch(1,3,curses.ACS_DIAMOND,val[3])
    else: stdscr.addstr(height-1,1,'tab: highlight / e: select')
    stdscr.addstr(height-1,width-89,'w: up / a: left / s: down / d: right / i: north / j: west/ k: south / l: east / q: quit')
    cy,cx=map(int,self.cell.split('.'))
    self.adjacents=['.'.join(map(str,[cy-1,cx])),'.'.join(map(str,[cy,cx+1])),'.'.join(map(str,[cy+1,cx])),'.'.join(map(str,[cy,cx-1]))]
    for adj in [a for a in self.adjacents if a in self.cells.keys()]:
      y,x={0:(0,3),1:(1,5),2:(2,3),3:(1,1)}[self.adjacents.index(adj)]
      if adj!='1.1':
        for num,val in self.links.iteritems():
          if val[2]==self.cells[adj]: color=val[3]
      else: color=curses.color_pair(1)
      stdscr.addch(y,x,curses.ACS_DIAMOND,color)
    stdscr.refresh()
  def navigate(self):
    self.textarea.chgat(self.links[self.count][0],self.links[self.count][1],len(self.links[self.count][2]),curses.A_REVERSE)
    if self.selected!=() and self.selected!=self.links[self.count]:
      self.textarea.chgat(self.selected[0],self.selected[1],len(self.selected[2]),self.selected[3])
    self.selected=self.links[self.count]
    if self.count<len(self.links)-1: self.count+=1
    else: self.count=0
  def select(self):
    r,g,b=self.config[self.selected[2]]
    curses.init_color(6-self.diacount,r,g,b)
    curses.init_pair(6-self.diacount,6-self.diacount,0)
    for num,val in self.links.iteritems():
      if val==self.selected:
        self.links[num]=(self.selected[0],self.selected[1],self.selected[2],curses.color_pair(6-self.diacount))
        self.selected=self.links[num]
    self.cells[self.cardinals[self.diacount]]=self.selected[2]
    self.diacount+=1
    self.drawinterface()
m = message()
def main(stdscr):
  os.system('setterm -cursor off')
  curses.init_color(1,1000,1000,1000)
  curses.init_pair(1,1,0) # base
  curses.init_color(2,500,500,500)
  curses.init_pair(2,2,0) # interface
  stdscr.bkgd(' ',curses.color_pair(2))
  kc=[ord('i'),ord('l'),ord('k'),ord('j')]
  m.load('1.1')
  while True:
    m.textarea.refresh(m.ypos,m.xpos,max(2,(height/2)-(m.h/2)),max(2,(width/2)-(m.w/2)),min(height-2,(height/2)+(m.h/2)),min(width-2,(width/2)+(m.w/2)))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and m.cell=='1.1': m.navigate()
    elif k==ord('e') and m.cell=='1.1' and m.diacount<len(m.cardinals) and m.selected[2] not in m.cells.values(): m.select()
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('d') and m.xpos+width<m.w: m.xpos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('a') and 0<m.xpos: m.xpos-=1
    elif k in kc and m.adjacents[kc.index(k)] in m.cells.keys(): m.load(m.adjacents[kc.index(k)])
  os.system('setterm -cursor on')
curses.wrapper(main)