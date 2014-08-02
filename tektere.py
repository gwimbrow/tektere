#! /usr/bin/env python
import sys,os,re,random,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    with open('log') as log: self.scenario=log.read().rstrip()
    self.mapped=False
    self.trail={}
  def reset(self,h,w):
    os.system('setterm -cursor off')
    self.h=h
    self.w=w
    self.ypos=0
    self.count=0
    self.links={}
    self.selection=()
    if 'textarea' in locals(): del self.textarea
    stdscr.clear()
    stdscr.bkgd(' ',curses.color_pair(4))
    stdscr.addstr(height-1,width-132,'tab: select / e: enter / m: map / q: quit / w: scroll up / s: scroll down / i: north, previous / l: east / k: south, next / j: west')
    self.textarea=curses.newpad(self.h,self.w)
    self.textarea.bkgd(' ',curses.color_pair(4))
  def load(self,verse):
    self.verse=verse
    self.trail[self.verse[:self.verse.index(':')+1]]=0
    if self.verse.endswith(':'):
      if self.verse=='1.1:':
        with open('/'.join(['data',self.scenario,'1.1','scene'])) as choice: script=choice.readlines()
      else: script=[''.join([self.verse,files]) for files in os.listdir('/'.join(['data',self.scenario,self.verse[:self.verse.index(':')]]))]
      self.reset(len(script),len(max(script,key=len)))
      c=map(int,self.verse[:-1].split('.'))
      self.occupied=[names+':' for names in os.listdir('/'.join(['data',self.scenario]))]
      self.adjacents=['.'.join(map(str,[c[0]-1,c[1]]))+':','.'.join(map(str,[c[0],c[1]+1]))+':','.'.join(map(str,[c[0]+1,c[1]]))+':','.'.join(map(str,[c[0],c[1]-1]))+':']
      arrows={0:(0,2),1:(1,4),2:(2,2),3:(1,0)}
      for adj in [a for a in self.adjacents if '-' not in a]:
        y,x=arrows[self.adjacents.index(adj)]
        if adj in self.occupied: stdscr.addch(y,x,curses.ACS_DIAMOND)
    else:
      with open('/'.join(['data',self.scenario,self.verse[:self.verse.index(':')],self.verse[self.verse.index(':')+1:]])) as choice: script=choice.readlines()
      self.reset(len(script),len(max(script,key=len)))
      self.occupied=[':'.join([self.verse[:self.verse.index(':')],files]) for files in os.listdir('/'.join(['data',self.scenario,self.verse[:self.verse.index(':')]]))]
      if self.occupied.index(self.verse)==0: prev=' '
      else:
        prev=self.occupied[self.occupied.index(self.verse)-1]
        stdscr.addch(2,width/2,curses.ACS_DIAMOND,curses.color_pair(3))
      if self.occupied.index(self.verse)==len(self.occupied)-1: adv=' '
      else:
        adv=self.occupied[self.occupied.index(self.verse)+1]
        stdscr.addch(height-2,width/2,curses.ACS_DIAMOND)
      self.adjacents=[prev,' ',adv,' ']
    stdscr.refresh()
    y=0
    for s in script:
      x=0
      for w in re.split('(\s+)',s.rstrip()):
        if ':' in w and w[:w.index(':')] in [names for names in os.listdir('/'.join(['data',self.scenario]))]:
          lp=w.split(':')
          if len([d for d in m.trail.items() if d[1]==1])==7: self.textarea.addstr(y,x,w,curses.color_pair(5))
          else: self.textarea.addstr(y,x,lp[1],curses.color_pair(2))
          self.links[self.count]=(y,x,lp[0]+':',lp[1])
          self.count+=1
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
    self.reset(9,18)
    stdscr.refresh()
    vseq=[1,4,7]
    hseq=[2,8,14]
    for c in [(vul-1,hul-1) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_HLINE)
    for c in [(vul-1,hul) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_HLINE)
    for c in [(vul-1,hul+1) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_HLINE)
    for c in [(vul-1,hul+2) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_URCORNER)
    for c in [(vul,hul+2) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_VLINE)
    for c in [(vul+1,hul+2) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_LRCORNER)
    for c in [(vul+1,hul-1) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_HLINE)
    for c in [(vul+1,hul) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_HLINE)
    for c in [(vul+1,hul+1) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_HLINE)
    for c in [(vul+1,hul-2) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_LLCORNER)
    for c in [(vul,hul-2) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_VLINE)
    for c in [(vul-1,hul-2) for vul in vseq for hul in hseq]: self.textarea.addch(c[0],c[1],curses.ACS_ULCORNER)
    for c in self.trail.keys():
      if self.trail[c]!=0:
        cy,cx=map(int,c[:-1].split('.'))
        self.textarea.addch(vseq[cy],hseq[cx],curses.ACS_DIAMOND,curses.color_pair(5))
m = message()
def main(stdscr):
  curses.init_color(1,1000,1000,1000)
  curses.init_pair(1,1,0) # base
  curses.init_color(2,1000,0,0)
  curses.init_pair(2,2,0) # link
  curses.init_color(3,0,1000,0)
  curses.init_pair(3,3,0) # selection, arrows
  curses.init_color(4,0,0,1000)
  curses.init_pair(4,4,0) # drawing
  curses.init_color(5,1000,800,0)
  curses.init_pair(5,5,0) # prize
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
      if address!=m.verse: m.trail[m.verse[:m.verse.index(':')+1]]=1
      if len([d for d in m.trail.items() if d[1]==1])==8:
        m.scenario=random.choice(os.listdir('data'))
        m.trail={}
        m.load('1.1:')
      else: m.load(address+target)
      address=''
      target=''
    elif k==ord('m'):
      if m.mapped==False: m.grid()
      else:
        m.mapped=False
        m.load(m.verse)
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k in kc and m.adjacents[kc.index(k)] in m.occupied:
      m.trail[m.verse]=0
      m.load(m.adjacents[kc.index(k)])
  with open('log','w') as log: log.write(m.scenario)
  os.system('setterm -cursor on')
curses.wrapper(main)