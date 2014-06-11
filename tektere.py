#! /usr/bin/env python
import os,re,curses,curses.textpad
from subprocess import call
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    self.keys=[ 'w: up / s: down / tab: select / e: enter / r: revise / q: quit','i: north, previous / l: east / k: south, next / j: west',
    ['first','second','third','fourth','fifth','sixth','seventh','eigth','ninth']]
  def reset(self,h,w,v):
    os.system('setterm -cursor off')
    self.h=h
    self.w=w
    self.ypos=0
    self.count=0
    self.links=[]
    self.selection=[]
    if 'textarea' in locals(): del self.textarea
    stdscr.clear()
    stdscr.addstr(height-1,0,self.keys[0])
    stdscr.addstr(height-1,width-len(self.keys[1])-1,self.keys[1])
    if v.endswith(':'):
      c=map(int,v[:v.index(':')].split('.'))
      self.occupied=[names+':' for names in os.listdir('data')]
      self.adjacents=['.'.join(map(str,[max(0,c[0]-1),c[1]]))+':','.'.join(map(str,[c[0],c[1]+1]))+':','.'.join(map(str,[c[0]+1,c[1]]))+':','.'.join(map(str,[c[0],max(0,c[1]-1)]))+':']
      if v[0]!='0':
        if m.adjacents[0] in m.occupied: stdscr.addch(2,width/2,curses.ACS_UARROW)
        else: stdscr.addch(2,width/2,curses.ACS_UARROW,curses.color_pair(3))
      if v[2]!='9':
        if m.adjacents[1] in m.occupied: stdscr.addch(height/2,width-2,curses.ACS_RARROW)
        else: stdscr.addch(height/2,width-2,curses.ACS_RARROW,curses.color_pair(3))
      if v[0]!='9':
        if m.adjacents[2] in m.occupied: stdscr.addch(height-2,width/2,curses.ACS_DARROW)
        else: stdscr.addch(height-2,width/2,curses.ACS_DARROW,curses.color_pair(3))
      if v[2]!='0':
        if m.adjacents[3] in m.occupied: stdscr.addch(height/2,2,curses.ACS_LARROW)
        else: stdscr.addch(height/2,2,curses.ACS_LARROW,curses.color_pair(3))
    else:
      self.occupied=sorted([':'.join([v[:v.index(':')],files]) for files in os.listdir('/'.join(['data',v[:v.index(':')]])) if files!='scene'])
      if self.occupied.index(v)==0: prev=' '
      else: prev=self.occupied[self.occupied.index(v)-1]
      try: adv=self.occupied[self.occupied.index(v)+1]
      except IndexError: adv=' '
      self.adjacents=[prev,' ',adv,' ']
      if m.adjacents[0] in m.occupied: stdscr.addch(2,width/2,curses.ACS_UARROW)
      if m.adjacents[2] in m.occupied: stdscr.addch(height-2,width/2,curses.ACS_DARROW)
    stdscr.refresh()
    self.textarea=curses.newpad(self.h,self.w)
    self.textarea.bkgd(' ',curses.color_pair(4))
    self.textarea.addstr(1,1,v[:v.index(':')+1],curses.color_pair(2))
    self.links.append([1,1,v[:v.index(':')+1]])
    self.textarea.addstr(1,6,v[v.index(':')+1:],curses.color_pair(1))
    self.textarea.addch(2,0,curses.ACS_LTEE)
    self.textarea.addch(2,self.w-1,curses.ACS_RTEE)
    self.textarea.hline(2,1,curses.ACS_HLINE,self.w-2)
  def load(self,verse):
    if verse.endswith(':'):
      with open('/'.join(['data',verse[:verse.index(':')],'scene'])) as choice: script=choice.readlines()
      script.extend('\n')
      script.extend(sorted([''.join(['Act the ',verse,files]) for files in os.listdir('/'.join(['data',verse[:verse.index(':')]])) if files!='scene']))
      script.extend('\n')
      n=[verse+f for f in self.keys[2] if ''.join(['Act the ',verse,f]) not in script]
      script.append(' '.join(['write of the',n[0],'encounter']))
    else:
      with open('/'.join(['data',verse[:verse.index(':')],verse[verse.index(':')+1:]])) as choice: script=choice.readlines()
    self.reset(len(script)+7,max(len(verse),len(max(script,key=len)))+3,verse)
    y=4
    for s in script:
      x=1
      if s.startswith('{'):
        with open('/'.join(['data',s[s.index('{')+1:s.index(':')],s[s.index(':')+1:s.index('}')]])) as quoted: quote=quoted.readlines()
        self.h=max(self.h,len(quote)+7)
        self.w=max(self.w,len(max(quote,key=len))+3)
        self.textarea.resize(self.h,self.w)
        for line in quote:
          self.textarea.addstr(y,x,line)
          y+=1
      else:
        for w in re.split('(\s+)',s.rstrip()):
          if ':' in w and w[:w.index(':')] in [names for names in os.listdir('data')]:
            if verse.endswith(':') and not w.endswith(':'): w=w[w.index(':')+1:]
            self.textarea.addstr(y,x,w,curses.color_pair(2))
            self.links.append([y,x,w])
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
  def revise(self,l):
    if l.endswith(':'):
      os.mkdir('/'.join(['data',l[:l.index(':')]]))
      with open('/'.join(['data',l[:l.index(':')],'scene']),'w') as scene: scene.write('scene '+l)
      call(['nano','-t','/'.join(['data',l[:l.index(':')],'scene'])])
      self.load(l)
    else:
      if l not in [files for files in os.listdir('/'.join(['data',self.textarea.instr(1,1,3)]))]:
        with open('/'.join(['data',self.textarea.instr(1,1,3),l]),'w') as newfile: newfile.write('newfile')
      call(['nano','-t','/'.join(['data',self.textarea.instr(1,1,3),l])])
      if l=='scene': l=''
      self.load(self.textarea.instr(1,1,4)+l)
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
  stdscr.bkgd(' ',curses.color_pair(4))
  with open('log') as log: m.load(log.read().rstrip())
  target=''
  kc=[ord('i'),ord('l'),ord('k'),ord('j')]
  while True:
    m.textarea.refresh(m.ypos,0,max(3,(height/2)-(m.h/2)),(width/2)-(m.w/2),min(height-3,(height/2)+(m.h/2)),(width/2)+(m.w/2))
    k=m.textarea.getch()
    if k==ord('q'): break
    elif k==ord('\t') and len(m.links)>0: target=m.navigate()
    elif k==ord('e') and target!='':
      if ':' not in target:
        try: m.load(m.textarea.instr(1,1,4)+target)
        except IOError: m.revise(target)
      else: m.load(target)
      target=''
    elif k==ord('r') and target!='':
      if target.endswith(':'): m.revise('scene')
      elif ':' not in target:
        m.revise(target)
        target=''
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k in kc:
      if m.adjacents[kc.index(k)] in m.occupied: m.load(m.adjacents[kc.index(k)])
      elif m.adjacents[kc.index(k)].endswith(':'): m.revise(m.adjacents[kc.index(k)])
  os.system('setterm -cursor on')
curses.wrapper(main)