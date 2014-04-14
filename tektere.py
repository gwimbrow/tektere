#! /usr/bin/env python
import sys,os,re,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self): self.tipline='tektere protocol v.4 / w: pg up / s: pg down / tab: select / e: enter / q: quit'
  def reset(self,h,w):
    stdscr.clear()
    stdscr.addstr(height-1,width-len(self.tipline)-1,self.tipline,curses.color_pair(1))
    stdscr.refresh()
    if 'textarea' in locals(): del self.textarea
    self.textarea=curses.newpad(h,w)
    self.textarea.bkgd(' ',curses.color_pair(1))
    self.ypos=0
    self.count=0
    self.links=[]
    self.selection=[]
  def load(self,address,timestamp=0):
    if '.' not in address:
      with open('/'.join([sys.path[0],'data',address])) as choice: script=choice.readlines()
      self.reset(len(script)+1,len(max(script,key=len))+1)
      y=0
    else:
      if timestamp==0:
        with open('log') as log: present=int(log.read().split(':')[1].rstrip())
        files=[int(names) for names in os.listdir('/'.join([sys.path[0],'data',address]))]
        if present>min(files): timestamp=max([f for f in files if f<present])
        else: timestamp=min(files)
      with open('/'.join([sys.path[0],'data',address,str(timestamp)])) as choice: script=choice.readlines()
      host=address.split('.')[1].rstrip()
      self.reset(len(script)+2,max(len(host),len(max(script,key=len)))+1)
      self.textarea.addstr(0,self.textarea.getmaxyx()[1]-len(host)-2,host,curses.color_pair(2))
      self.textarea.addch(0,self.textarea.getmaxyx()[1]-1,curses.ACS_DARROW,curses.color_pair(1))
      self.links.append([0,self.textarea.getmaxyx()[1]-len(host)-2,host])
      y=2
    for s in script:
      x=0
      for w in re.split('(\s+)',s.rstrip()):
        if w.startswith('{'):
          y+=1
          quote=w[1:-1].split(':')
          with open('/'.join([sys.path[0],'data',quote[0],quote[1]])) as quoted: lines=[line for line in quoted.readlines() if not line.startswith('{')]
          host=quote[0].split('.')[1].rstrip()
          self.textarea.resize(max(self.textarea.getmaxyx()[0],self.textarea.getmaxyx()[0]+len(lines)+3),max([self.textarea.getmaxyx()[1],len(host)+1,len(max(lines,key=len))+1]))
          self.textarea.addstr(y,self.textarea.getmaxyx()[1]-len(host)-2,host,curses.color_pair(2))
          self.textarea.addch(y,self.textarea.getmaxyx()[1]-1,curses.ACS_DARROW,curses.color_pair(4))
          self.links.append([y,self.textarea.getmaxyx()[1]-len(host)-2,host])
          y+=2
          for l in lines:
            self.textarea.addstr(y,0,l,curses.color_pair(4))
            y+=1
        elif w.lower() in [names.lower() for names in os.listdir(sys.path[0]+'/data')]:
          self.textarea.addstr(y,x,w,curses.color_pair(2))
          self.links.append([y,x,w.lower()])
          x+=len(w)
        else:
          for c in w:
            if c=='@': self.textarea.addch(y,x,curses.ACS_ULCORNER,curses.color_pair(4))
            elif c=='#': self.textarea.addch(y,x,curses.ACS_URCORNER,curses.color_pair(4))
            elif c=='$': self.textarea.addch(y,x,curses.ACS_LLCORNER,curses.color_pair(4))
            elif c=='%': self.textarea.addch(y,x,curses.ACS_LRCORNER,curses.color_pair(4))
            elif c=='|': self.textarea.addch(y,x,curses.ACS_VLINE,curses.color_pair(4))
            elif c=='_': self.textarea.addch(y,x,curses.ACS_HLINE,curses.color_pair(4))
            else: self.textarea.addch(y,x,c,curses.color_pair(1))
            x+=1
      y+=1
    if '.' in address:
      with open('log','w') as log: log.write(address+':'+str(timestamp))
  def navigate(self):
    self.textarea.chgat(self.links[self.count][0],self.links[self.count][1]-1,len(self.links[self.count][2])+2,curses.color_pair(3))
    if self.selection!=[] and self.selection!=self.links[self.count]: self.textarea.chgat(self.selection[0],self.selection[1]-1,len(self.selection[2])+2,curses.color_pair(2))
    self.selection=self.links[self.count]
    if self.count<len(self.links)-1: self.count+=1
    else: self.count=0
    return self.selection[2]
m = message()
def main(stdscr):
  global height,width
  curses.init_color(1,1000,1000,1000)
  curses.init_color(2,180,90,20)
  curses.init_pair(1,2,1) # base
  curses.init_color(3,1000,106,255)
  curses.init_pair(2,3,1) # link
  curses.init_color(4,0,953,396)
  curses.init_pair(3,1,4) # selection
  curses.init_color(5,275,39,1000)
  curses.init_pair(4,5,1) # quote / box drawing
  stdscr.bkgd(' ',curses.color_pair(1))
  curses.curs_set(0)
  with open('log') as log: save=log.read().rstrip().split(':')
  m.load(save[0],save[1])
  target=''
  while True:
    m.textarea.refresh(m.ypos,0,max(0,(height/2)-(m.textarea.getmaxyx()[0]/2)),(width/2)-(m.textarea.getmaxyx()[1]/2),min(height-2,(height/2)+(m.textarea.getmaxyx()[0]/2)),(width/2)+(m.textarea.getmaxyx()[1]/2))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and len(m.links)>0: target=m.navigate()
    elif k==ord('e') and target!='':
      m.load(target)
      target=''
    elif k==ord('s') and m.ypos+height<m.textarea.getmaxyx()[0]: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
  curses.curs_set(1)
curses.wrapper(main)