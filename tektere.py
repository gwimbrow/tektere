#! /usr/bin/env python
import os,re,ast,itertools,time,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    self.cardinals=['1.2','1.0','0.1']
    self.coordinates={'0.1':(1,6),'0.0':(2,2),'1.0':(4,2),'2.1':(5,6),'1.2':(4,10),'0.2':(2,10)}
    self.trigrams=[(),(1,1,1),(2,1,1),(1,2,1),(2,2,1),(1,1,2),(2,1,2),(1,2,2),(2,2,2)]
    self.config={'null':(500,500,500,8)}
    for f in os.listdir('data'):
      with open('/'.join(['data',f])) as file: self.config[f]=ast.literal_eval(file.readline().rstrip())
  def load(self,cell):
    self.cell=cell
    self.ypos=0
    self.xpos=0
    self.count=0
    self.diacount=1
    if 'textarea' in locals(): del self.textarea
    stdscr.clear()
    if self.cell=='1.1':
      self.links={}
      self.selected=()
      self.cells={'1.1':'null'}
      script=[f for f in self.config.keys() if f!='null']
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
          self.links[self.count]=(y,x,w,curses.color_pair(0))
          self.count+=1
        self.textarea.addstr(y,x,w,curses.color_pair(0))
        x+=len(w)
      y+=1
    self.count=0
    self.drawinterface()
  def drawinterface(self):
    if len(self.cells.items())>=len(self.cardinals)+1:
      calc=list([i for i in itertools.combinations([j for j in self.cardinals if j in self.cells.keys()],2)])
      for cmb in calc:
        corner='.'.join([cmb[0][-1],cmb[1][0]])
        if corner=='2.0': corner='0.2'
        saught=tuple(map(lambda di: min(di),zip(self.trigrams[self.config[self.cells[cmb[0]]][3]],self.trigrams[self.config[self.cells[cmb[1]]][3]])))
        for name,val in self.config.iteritems():
          if val[3]==self.trigrams.index(saught) and name not in self.cells.values(): self.cells[corner]=name
    for l in range(len(self.trigrams[self.config[self.cells[self.cell]][3]])):
      if self.trigrams[self.config[self.cells[self.cell]][3]][l]==1: stdscr.vline(height-4,width-(2+l*2),curses.ACS_BLOCK,3)
      else:
        stdscr.vline(height-4,width-(2+l*2),curses.ACS_BLOCK,1)
        stdscr.vline(height-2,width-(2+l*2),curses.ACS_BLOCK,1)
    for adj in [a for a in self.coordinates.keys() if a in self.cells.keys()]:
      y,x=self.coordinates[adj]
      if self.cell=='1.1':
        for num,val in self.links.iteritems():
          if val[2]==self.cells[adj]: color=val[3]
      else:
        r,g,b,t=self.config[self.cells[adj]]
        curses.init_color(self.diacount,r,g,b)
        curses.init_pair(self.diacount,self.diacount,0)
        color=curses.color_pair(self.diacount)
        self.diacount+=1
      stdscr.addch(y,x,curses.ACS_DIAMOND,color)
    stdscr.refresh()
    time.sleep(3)
    if len(self.cells.items())==len(self.coordinates.items())+1: self.load('1.1')
    else: self.load('1.1')
  def navigate(self):
    self.textarea.chgat(self.links[self.count][0],self.links[self.count][1],len(self.links[self.count][2]),curses.A_REVERSE)
    if self.selected!=() and self.selected!=self.links[self.count]:
      self.textarea.chgat(self.selected[0],self.selected[1],len(self.selected[2]),self.selected[3])
    self.selected=self.links[self.count]
    if self.count<len(self.links)-1: self.count+=1
    else: self.count=0
  def select(self):
    r,g,b,t=self.config[self.selected[2]]
    curses.init_color(self.diacount,r,g,b)
    curses.init_pair(self.diacount,self.diacount,0)
    for num,val in self.links.iteritems():
      if val==self.selected:
        self.links[num]=(self.selected[0],self.selected[1],self.selected[2],curses.color_pair(self.diacount))
        self.selected=self.links[num]
    self.cells[self.cardinals[len(self.cardinals)-self.diacount]]=self.selected[2]
    self.diacount+=1
    self.drawinterface()
m = message()
def main(stdscr):
  os.system('setterm -cursor off')
  stdscr.bkgd(' ',curses.color_pair(0))
  m.load('1.1')
  while True:
    m.textarea.refresh(m.ypos,m.xpos,max(2,(height/2)-(m.h/2)),max(2,(width/2)-(m.w/2)),min(height-2,(height/2)+(m.h/2)),min(width-2,(width/2)+(m.w/2)))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and m.cell=='1.1': m.navigate()
    elif k==ord('e') and m.cell=='1.1' and len(m.cells.items())<len(m.cardinals)+1: m.select()
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('d') and m.xpos+width<m.w: m.xpos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('a') and 0<m.xpos: m.xpos-=1
    elif k==ord('r'): m.load('1.1')
  os.system('setterm -cursor on')
curses.wrapper(main)