#! /usr/bin/env python
import sys,os,re,curses,string
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self): self.tipline='w: pg up / s: pg down / tab: select / e: enter / q: quit'
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
  def load(self,verse):
    if verse.endswith(':'):
      script=sorted([''.join([verse,files]) for files in os.listdir('/'.join([sys.path[0],'data',verse.replace(':','')]))])
      c=map(int,verse.replace(':','').split('.'))
      self.occupied=[names+':' for names in os.listdir('/'.join([sys.path[0],'data']))]
      self.adjacents=['.'.join(map(str,[c[0]-1,c[1]]))+':','.'.join(map(str,[c[0],c[1]+1]))+':','.'.join(map(str,[c[0]+1,c[1]]))+':','.'.join(map(str,[c[0],c[1]-1]))+':']
    else:
      address=verse.split(':')
      with open('/'.join([sys.path[0],'data',address[0],address[1]])) as choice: script=choice.readlines()
      self.occupied=sorted([':'.join([address[0],files]) for files in os.listdir('/'.join([sys.path[0],'data',address[0]]))])
      self.adjacents=[self.occupied[max(0,self.occupied.index(verse)-1)],' ',self.occupied[min(len(self.occupied)-1,self.occupied.index(verse)+1)],' ']
    self.reset(len(script)+1,len(max(script,key=len))+1)
    y=0
    for s in script:
      x=0
      for w in re.split('(\s+)',s.rstrip()):
        if ':' in w and w.split(':')[0] in [names for names in os.listdir(sys.path[0]+'/data')]:
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
    with open('log','w') as log: log.write(verse)
  def navigate(self):
    self.textarea.chgat(self.links[self.count][0],self.links[self.count][1],len(self.links[self.count][2]),curses.color_pair(3))
    if self.selection!=[] and self.selection!=self.links[self.count]: self.textarea.chgat(self.selection[0],self.selection[1],len(self.selection[2]),curses.color_pair(2))
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
  curses.init_pair(3,4,1) # selection
  curses.init_color(5,275,39,1000)
  curses.init_pair(4,5,1) # quote / box drawing
  stdscr.bkgd(' ',curses.color_pair(1))
  curses.curs_set(0)
  with open('log') as log: m.load(log.read().rstrip())
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
    elif k==ord('i') and m.adjacents[0] in m.occupied: m.load(m.adjacents[0])
    elif k==ord('l') and m.adjacents[1] in m.occupied: m.load(m.adjacents[1])
    elif k==ord('k') and m.adjacents[2] in m.occupied: m.load(m.adjacents[2])
    elif k==ord('j') and m.adjacents[3] in m.occupied: m.load(m.adjacents[3])
  curses.curs_set(1)
curses.wrapper(main)