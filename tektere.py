#! /usr/bin/env python
import os,re,ast,itertools,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    self.cardinals=['0.1','1.2','2.1','1.0']
    self.trigrams=[(),(1,1,1),(2,1,1),(1,2,1),(2,2,1),(1,1,2),(2,1,2),(1,2,2),(2,2,2)]
    self.config={'null':(500,500,500,0)}
    for f in os.listdir('data'):
      with open('/'.join(['data',f])) as file: self.config[f]=ast.literal_eval(file.readline().rstrip())
  def load(self,cell):
    self.cell=cell
    self.ypos=0
    self.xpos=0
    self.count=0
    self.diacount=len(self.cardinals)
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
  def calculate(self):
    calc=list([i for i in itertools.combinations([j for j in self.cardinals if j in self.cells.keys()],2) if self.cardinals.index(i[0])+1==self.cardinals.index(i[1]) or self.cardinals.index(i[1])-self.cardinals.index(i[0])==len(self.cardinals)-1])
    if ('0.1','1.0') in calc: calc.append(calc.pop(calc.index(('0.1','1.0')))[::-1])
    x=[0,-1]
    for cmb in calc:
      corner='.'.join([cmb[0][x[0]],cmb[1][x[1]]])
      x=x[::-1]
      saught=tuple(map(lambda di: min(di),zip(self.trigrams[self.config[self.cells[cmb[0]]][3]],self.trigrams[self.config[self.cells[cmb[1]]][3]])))
      for name,val in self.config.iteritems():
        if val[3]==self.trigrams.index(saught) and name not in self.cells.values(): self.cells[corner]=name
  def drawinterface(self):
    stdscr.addstr(height-1,width-88,'w: up / a: left / s: down / d: right / i: north / j: west/ k: south / l: east / q: quit')
    r,g,b,t=self.config[self.cells[self.cell]]
    if self.cell=='1.1': stdscr.addstr(height-1,1,'tab: highlight / e: select')
    else:
      self.calculate()
      curses.init_color(1,r,g,b)
      curses.init_pair(1,1,0)
      stdscr.attron(curses.color_pair(1))
    stdscr.addch(1,3,curses.ACS_DIAMOND)
    for l in range(len(self.trigrams[t])):
      if self.trigrams[t][l]==1: stdscr.vline(height/2,width-(2+l*2),curses.ACS_BLOCK,3)
      else:
        stdscr.vline(height/2,width-(2+l*2),curses.ACS_BLOCK,1)
        stdscr.vline(height/2+2,width-(2+l*2),curses.ACS_BLOCK,1)
    cy,cx=map(int,self.cell.split('.'))
    self.adjacents=['.'.join(map(str,[cy-1,cx])),'.'.join(map(str,[cy,cx+1])),'.'.join(map(str,[cy+1,cx])),'.'.join(map(str,[cy,cx-1]))]
    for adj in [a for a in self.adjacents if a in self.cells.keys()]:
      y,x={0:(0,3),1:(1,5),2:(2,3),3:(1,1)}[self.adjacents.index(adj)]
      if self.cell=='1.1':
        for num,val in self.links.iteritems():
          if val[2]==self.cells[adj]: color=val[3]
      else:
        stdscr.attroff(curses.color_pair(1))
        r,g,b,t=self.config[self.cells[adj]]
        curses.init_color(self.diacount,r,g,b)
        curses.init_pair(self.diacount,self.diacount,0)
        color=curses.color_pair(self.diacount)
        self.diacount-=1
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
    r,g,b,t=self.config[self.selected[2]]
    curses.init_color(self.diacount,r,g,b)
    curses.init_pair(self.diacount,self.diacount,0)
    for num,val in self.links.iteritems():
      if val==self.selected:
        self.links[num]=(self.selected[0],self.selected[1],self.selected[2],curses.color_pair(self.diacount))
        self.selected=self.links[num]
    self.cells[self.cardinals[len(self.cardinals)-self.diacount]]=self.selected[2]
    self.diacount-=1
    self.drawinterface()
m = message()
def main(stdscr):
  os.system('setterm -cursor off')
  stdscr.bkgd(' ',curses.color_pair(0))
  kc=[ord('i'),ord('l'),ord('k'),ord('j')]
  m.load('1.1')
  while True:
    m.textarea.refresh(m.ypos,m.xpos,max(2,(height/2)-(m.h/2)),max(2,(width/2)-(m.w/2)),min(height-2,(height/2)+(m.h/2)),min(width-2,(width/2)+(m.w/2)))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and m.cell=='1.1': m.navigate()
    elif k==ord('e') and m.cell=='1.1' and (len(m.cardinals)-m.diacount)<len(m.cardinals) and m.selected[2] not in m.cells.values(): m.select()
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('d') and m.xpos+width<m.w: m.xpos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k==ord('a') and 0<m.xpos: m.xpos-=1
    elif k in kc and m.adjacents[kc.index(k)] in m.cells.keys(): m.load(m.adjacents[kc.index(k)])
  os.system('setterm -cursor on')
curses.wrapper(main)