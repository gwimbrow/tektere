#! /usr/bin/env python
import sys,os,re,string,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    with open('log') as log: self.scenario=log.read().rstrip()
    self.mapped=False
    self.trail={}
  def reset(self,h,w):
    self.h=h
    self.w=w
    self.ypos=0
    self.count=0
    self.links={}
    self.selection=()
    if 'textarea' in locals(): del self.textarea
    stdscr.clear()
    stdscr.addstr(height-1,width-132,'tab: select / e: enter / m: map / q: quit / w: scroll up / s: scroll down / i: north, previous / l: east / k: south, next / j: west')
    self.textarea=curses.newpad(self.h,self.w)
    self.textarea.bkgd(' ',curses.color_pair(4))
  def load(self,v):
    self.verse=v
    self.trail[self.verse[:self.verse.index(':')+1]]=0
    if self.verse.endswith(':'): f='scene'
    else: f=self.verse[self.verse.index(':')+1:]
    with open('/'.join(['data',self.scenario,self.verse[:self.verse.index(':')],f])) as choice: script=choice.readlines()
    self.reset(len(script),len(max(script,key=len)))
    cy,cx=map(int,self.verse[:self.verse.index(':')].split('.'))
    self.adjacents=['.'.join(map(str,[cy-1,cx])),'.'.join(map(str,[cy,cx+1])),'.'.join(map(str,[cy+1,cx])),'.'.join(map(str,[cy,cx-1]))]
    for adj in [a for a in self.adjacents if '-' not in a]:
      y,x={0:(0,2),1:(1,4),2:(2,2),3:(1,0)}[self.adjacents.index(adj)]
      stdscr.addch(y,x,curses.ACS_DIAMOND)
    stdscr.refresh()
    y=0
    for s in script:
      x=0
      for w in re.split('(\s+)',s.rstrip()):
        if ':' in w and w[w.index(':')+1:] in [names for names in os.listdir('/'.join(['data',self.scenario,w[:w.index(':')]]))]:
            if len([d for d in m.trail.items() if d[1]==1])==7: self.textarea.addstr(y,x,w[w.index(':')+1:],curses.color_pair(5))
            else: self.textarea.addstr(y,x,w[w.index(':')+1:],curses.color_pair(2))
            self.links[self.count]=(y,x,w[:w.index(':')+1],w[w.index(':')+1:])
            self.count+=1
        elif w.startswith('[') and w.endswith(']'): self.textarea.addstr(y,x,w,curses.color_pair(6))
        else: self.textarea.addstr(y,x,w,curses.color_pair(1))
        x+=len(w)
      y+=1
    self.count=0
  def navigate(self):
    self.textarea.chgat(self.links[self.count][0],self.links[self.count][1],len(self.links[self.count][3]),curses.color_pair(3))
    if self.selection!=() and self.selection!=self.links[self.count]: self.textarea.chgat(self.selection[0],self.selection[1],len(self.selection[3]),curses.color_pair(2))
    self.selection=self.links[self.count]
    if self.count<len(self.links)-1: self.count+=1
    else: self.count=0
    return self.selection[2],self.selection[3]
  def grid(self):
    self.mapped=True
    self.reset(11,22)
    stdscr.addstr(0,0,self.scenario)
    stdscr.refresh()
    vseq=[1,5,9]
    hseq=[2,10,18]
    cy,cx=map(int,self.verse[:self.verse.index(':')].split('.'))
    self.textarea.addstr(vseq[cy],hseq[cx]-1,self.verse[:self.verse.index(':')],curses.color_pair(2))
    self.links[0]=(vseq[cy],hseq[cx]-1,self.verse[:self.verse.index(':')+1],self.verse[:self.verse.index(':')])
    for c in self.trail.keys():
      if self.trail[c]!=0:
        cy,cx=map(int,c[:-1].split('.'))
        self.textarea.addstr(vseq[cy],hseq[cx]-1,c[:-1],curses.color_pair(5))
m = message()
def main(stdscr):
  os.system('setterm -cursor off')
  curses.init_color(1,1000,1000,1000)
  curses.init_pair(1,1,0) # base
  curses.init_color(2,1000,0,0)
  curses.init_pair(2,2,0) # link
  curses.init_color(3,0,1000,0)
  curses.init_pair(3,3,0) # selection
  curses.init_color(4,0,0,1000)
  curses.init_pair(4,4,0) # interface
  curses.init_color(5,1000,800,0)
  curses.init_pair(5,5,0) # prize
  curses.init_color(6,500,500,500)
  curses.init_pair(6,6,6) # redacted
  stdscr.bkgd(' ',curses.color_pair(4))
  address=''
  target=''
  kc=[ord('i'),ord('l'),ord('k'),ord('j')]
  m.load('1.1:')
  while True:
    m.textarea.refresh(m.ypos,0,max(3,(height/2)-(m.h/2)),(width/2)-(m.w/2),min(height-3,(height/2)+(m.h/2)),(width/2)+(m.w/2))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and len(m.links)>0: address,target=m.navigate()
    elif k==ord('e') and target!='':
      if m.mapped==False and len([d for d in m.trail.items() if d[1]==1])==7:
        m.scenario=str(int(m.scenario)+1)
        m.trail={}
        m.load('1.1:')
      elif address==target+':':
        if m.mapped==True: m.mapped=False
        m.load(address)
      else:
        if address not in m.verse: m.trail[m.verse[:m.verse.index(':')+1]]=1
        m.load(address+target)
      address=''
      target=''
    elif k==ord('m') and m.mapped==False: m.grid()
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k in kc: m.load(m.adjacents[kc.index(k)]+':')
  with open('log','w') as log: log.write(m.scenario)
  os.system('setterm -cursor on')
curses.wrapper(main)