#! /usr/bin/env python
import sys,os,re,curses,string
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self): self.tipline='w: pg up / s: pg down / tab: select / e: enter / q: quit'
  def reset(self,h,w):
    stdscr.clear()
    stdscr.addstr(height-1,width-len(self.tipline)-1,self.tipline)
    stdscr.refresh()
    if 'textarea' in locals(): del self.textarea
    self.h=h
    self.w=w
    self.textarea=curses.newpad(self.h,self.w)
    self.textarea.bkgd(' ',curses.color_pair(4))
    self.textarea.addch(2,0,curses.ACS_LTEE)
    self.textarea.addch(2,self.w-1,curses.ACS_RTEE)
    self.textarea.hline(2,1,curses.ACS_HLINE,self.w-2)
    self.ypos=0
    self.count=0
    self.links=[]
    self.selection=[]
  def load(self,verse):
    if verse.endswith(':'):
      with open('/'.join([sys.path[0],'data',verse[:verse.index(':')],verse[:verse.index(':')]])) as choice: script=choice.readlines()
      script.extend('\n')
      script.extend([''.join([verse,files]) for files in os.listdir('/'.join([sys.path[0],'data',verse[:verse.index(':')]])) if files!=verse[:verse.index(':')]])
      c=map(int,verse[:verse.index(':')].split('.'))
      self.occupied=[names+':' for names in os.listdir('/'.join([sys.path[0],'data']))]
      self.adjacents=['.'.join(map(str,[c[0]-1,c[1]]))+':','.'.join(map(str,[c[0],c[1]+1]))+':','.'.join(map(str,[c[0]+1,c[1]]))+':','.'.join(map(str,[c[0],c[1]-1]))+':']
    else:
      with open('/'.join([sys.path[0],'data',verse[:verse.index(':')],verse[verse.index(':')+1:len(verse)]])) as choice: script=choice.readlines()
      self.occupied=sorted([':'.join([verse[:verse.index(':')],files]) for files in os.listdir('/'.join([sys.path[0],'data',verse[:verse.index(':')]])) if files!=verse[:verse.index(':')]])
      self.adjacents=[self.occupied[max(0,self.occupied.index(verse)-1)],' ',self.occupied[min(len(self.occupied)-1,self.occupied.index(verse)+1)],' ']
    self.reset(len(script)+7,len(max(script,key=len))+3)
    self.textarea.addstr(1,1,verse[:verse.index(':')+1],curses.color_pair(2))
    self.links.append([1,1,verse[:verse.index(':')+1]])
    self.textarea.addstr(1,len(verse[:verse.index(':')])+3,verse[verse.index(':')+1:len(verse)],curses.color_pair(1))
    y=4
    for s in script:
      x=1
      if s.startswith('{'):
        with open('/'.join([sys.path[0],'data',s[s.index('{')+1:s.index(':')],s[s.index(':')+1:s.index('}')]])) as quoted: quote=quoted.readlines()
        self.h=max(self.h,len(quote)+7)
        self.w=max(self.w,len(max(quote,key=len))+3)
        self.textarea.resize(self.h,self.w)
        for line in quote:
          self.textarea.addstr(y,x,line)
          y+=1
      else:
        for w in re.split('(\s+)',s.rstrip()):
          if ':' in w and w[:w.index(':')] in [names for names in os.listdir(sys.path[0]+'/data')]:
            self.textarea.addstr(y,x,w,curses.color_pair(2))
            self.links.append([y,x,w.lower()])
            x+=len(w)
          else:
            for c in w:
              if c=='@': self.textarea.addch(y,x,curses.ACS_ULCORNER)
              elif c=='#': self.textarea.addch(y,x,curses.ACS_URCORNER)
              elif c=='$': self.textarea.addch(y,x,curses.ACS_LLCORNER)
              elif c=='%': self.textarea.addch(y,x,curses.ACS_LRCORNER)
              elif c=='|': self.textarea.addch(y,x,curses.ACS_VLINE)
              elif c=='_': self.textarea.addch(y,x,curses.ACS_HLINE)
              else: self.textarea.addch(y,x,c,curses.color_pair(1))
              x+=1
        y+=1
    self.textarea.addch(y+1,0,curses.ACS_LTEE)
    self.textarea.addch(y+1,self.w-1,curses.ACS_RTEE)
    self.textarea.hline(y+1,1,curses.ACS_HLINE,self.w-2)
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
  curses.init_pair(1,1,0) # base
  curses.init_color(3,1000,106,255)
  curses.init_pair(2,3,0) # link
  curses.init_color(4,0,953,396)
  curses.init_pair(3,4,0) # selection
  curses.init_color(5,275,39,1000)
  curses.init_pair(4,5,0) # box drawing
  stdscr.bkgd(' ',curses.color_pair(1))
  curses.curs_set(0)
  with open('log') as log: m.load(log.read().rstrip())
  target=''
  while True:
    m.textarea.refresh(m.ypos,0,max(0,(height/2)-(m.h/2)),(width/2)-(m.w/2),min(height-2,(height/2)+(m.h/2)),(width/2)+(m.w/2))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and len(m.links)>0: target=m.navigate()
    elif k==ord('e') and target!='':
      m.load(target)
      target=''
    elif k==ord('s') and m.ypos+height<m.h: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('i') and m.adjacents[0] in m.occupied: m.load(m.adjacents[0])
    elif k==ord('l') and m.adjacents[1] in m.occupied: m.load(m.adjacents[1])
    elif k==ord('k') and m.adjacents[2] in m.occupied: m.load(m.adjacents[2])
    elif k==ord('j') and m.adjacents[3] in m.occupied: m.load(m.adjacents[3])
  curses.curs_set(1)
curses.wrapper(main)