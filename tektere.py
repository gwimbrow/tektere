#! /usr/bin/env python
import sys,os,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    self.fresh=True
  def reset(self,th,tw):
    stdscr.clear()
    stdscr.refresh()
    if 'textarea' in locals(): del self.textarea
    self.textarea=curses.newpad(th,tw)
    self.textarea.bkgd(' ',curses.color_pair(3))
    self.ypos=0
    self.xpos=0
    self.count=0
    self.links=[]
    self.selection=[]
  def load(self,sub):
    with open('log') as log: present=int(log.read().split(':')[1].rstrip())
    if self.fresh==True:
      timestamp=str(present)
      self.fresh = False
    else:
      files=[int(names) for names in os.listdir('/'.join([sys.path[0],'data',sub]))]
      if present<max(files):
        files.sort()
        for f in files:
          if f>present:
            timestamp=f
            break
      else: timestamp=max(files)
    with open('/'.join([sys.path[0],'data',sub,str(timestamp)])) as choice: script=choice.readlines()
    self.reset(len(script)+6,len(max(script,key=len))+6)
    y=2
    for s in script:
      if s.startswith('{'):
        quote=s.rstrip()[1:-1].split(':')
        with open('/'.join([sys.path[0],'data',quote[0],quote[1]])) as quoted: lines=[line for line in quoted.readlines() if not line.startswith('{')]
        self.textarea.resize(max(self.textarea.getmaxyx()[0],self.textarea.getmaxyx()[0]+len(lines)),max(self.textarea.getmaxyx()[1],len(max(lines,key=len))+6))
        for l in lines:
          self.textarea.addstr(y,3,l,curses.color_pair(4))
          y+=1
      else:
        x=3
        y+=1
        for w in s.rstrip().split(' '):
          if w.lower() in [names.lower() for names in os.listdir(sys.path[0]+'/data')]:
            self.textarea.addstr(y,x,w,curses.color_pair(1))
            self.links.append([y,x,w.lower()])
          else: self.textarea.addstr(y,x,w)
          x+=len(w)+1
    self.textarea.addstr(self.textarea.getmaxyx()[0]-2,self.textarea.getmaxyx()[1]-len(str(timestamp))-2,str(timestamp))
    with open('log','w') as log: log.write(sub+':'+str(timestamp))
  def navigate(self):
    self.textarea.chgat(self.links[self.count][0],self.links[self.count][1],len(self.links[self.count][2]),curses.color_pair(2))
    if self.selection!=[] and self.selection!=self.links[self.count]: self.textarea.chgat(self.selection[0],self.selection[1],len(self.selection[2]),curses.color_pair(1))
    self.selection=self.links[self.count]
    if self.count<len(self.links)-1: self.count+=1
    else: self.count=0
    return self.selection[2]
  def history(self):
    with open('log') as log: archive=log.read().rstrip().split(':')
    script=[names for names in os.listdir('/'.join([sys.path[0],'data',archive[0]])) if int(names)<=int(archive[1])]
    self.reset(len(script)+6,len(max(script,key=len))+6)
    self.fresh=True
    for i in range(len(script)):
      self.textarea.addstr(i+2,3,script[i],curses.color_pair(1))
      self.links.append([i+2,3,script[i]])
    return archive[0]
m = message()
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
  with open('log') as log: m.load(log.read().split(':')[0])
  target=''
  user=''
  while True:
    m.textarea.refresh(m.ypos,m.xpos,max(0,(height/2)-(m.textarea.getmaxyx()[0]/2)),max(0,(width/2)-(m.textarea.getmaxyx()[1]/2)),min(height-1,(height/2)+(m.textarea.getmaxyx()[0]/2)),min(width-1,(width/2)+(m.textarea.getmaxyx()[1]/2)))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and len(m.links)>0: target=m.navigate()
    elif k==ord('e') and target!='':
      if m.fresh==True:
        with open('log','w') as log: log.write(user+':'+target)
        m.load(user)
      else: m.load(target)
      target=''
    elif k==ord('r') and m.fresh==False:
      user=m.history()
      target=''
    elif k==ord('s') and m.ypos+height<m.textarea.getmaxyx()[0]: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('d') and m.xpos+width<m.textarea.getmaxyx()[1]: m.xpos+=1
    elif k==ord('a') and 0<m.xpos: m.xpos-=1
  curses.curs_set(1)
curses.wrapper(main)