# To do: create an additional folder subdirectory below the /data dir that will contain the folders for different scenarios.
# When a scenario is loaded, reset the dict stored in the log file to {}.
# Load a config file from the scenario folder which contains color information and a dictionary sequence to compare with the dict in the log file.
# Use if len(set(self.trail.items()) & set(self.scenario.items()))==len(scenario.items()):
# to check if the dicts have all the same values and same number of values. if true, then load the next scenario.
# The scenario folders will be numbered sequentially. Display the scenario number at the top-left corner of the screen (above the UARROW)
#
#! /usr/bin/env python
import sys,os,re,ast,getopt,curses
from subprocess import call
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class message:
  def __init__(self):
    self.write=False
    options,rmd=getopt.getopt(sys.argv[1:],'w')
    for opt,arg in options:
      if opt=='-w': self.write=True
    self.keys=[ 'w: up / s: down / tab: select / e: enter / q: quit',' / r: revise','i: north, previous / l: east / k: south, next / j: west',['I','II','III','IV','V']]
  def reset(self,h,w):
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
    if self.write==True: stdscr.addstr(height-1,len(self.keys[0])+1,self.keys[1])
    stdscr.addstr(height-1,width-len(self.keys[2])-1,self.keys[2])
    self.textarea=curses.newpad(self.h,self.w)
    self.textarea.bkgd(' ',curses.color_pair(4))
  def load(self,verse):
    with open('log') as log: self.trail=ast.literal_eval(log.readlines()[1].rstrip())
    if verse.endswith(':'):
      with open('/'.join(['data',verse[:verse.index(':')],'scene'])) as choice: script=choice.readlines()
      script.extend('\n')
      script.extend(sorted([''.join(['Act ',verse,files]) for files in os.listdir('/'.join(['data',verse[:verse.index(':')]])) if files!='scene']))
      script.extend('\n')
      n=[verse+f for f in self.keys[3] if ''.join(['Act ',verse,f]) not in script]
      if self.write==True: script.append('write '+n[0])
      self.reset(len(script)+7,max(len(verse),len(max(script,key=len)))+3)
      c=map(int,verse[:verse.index(':')].split('.'))
      self.occupied=[names+':' for names in os.listdir('data')]
      self.adjacents=['.'.join(map(str,[max(0,c[0]-1),c[1]]))+':','.'.join(map(str,[c[0],c[1]+1]))+':','.'.join(map(str,[c[0]+1,c[1]]))+':','.'.join(map(str,[c[0],max(0,c[1]-1)]))+':']
      if verse[0]!='0':
        if verse in self.trail.keys() and self.trail[verse]==0: stdscr.addch(2,width/2,curses.ACS_UARROW)
        elif self.adjacents[0] in self.occupied: stdscr.addch(2,width/2,curses.ACS_UARROW,curses.color_pair(3))
        elif self.write==True: stdscr.addch(2,width/2,curses.ACS_UARROW,curses.color_pair(2))
      if verse[2]!=min(9,len(self.occupied)-1):
        if verse in self.trail.keys() and self.trail[verse]==1: stdscr.addch(height/2,width-2,curses.ACS_RARROW)
        elif self.adjacents[1] in self.occupied: stdscr.addch(height/2,width-2,curses.ACS_RARROW,curses.color_pair(3))
        elif self.write==True: stdscr.addch(height/2,width-2,curses.ACS_RARROW,curses.color_pair(2))
      if verse[0]!=min(9,len(self.occupied)-1):
        if verse in self.trail.keys() and self.trail[verse]==2: stdscr.addch(height-2,width/2,curses.ACS_DARROW)
        elif self.adjacents[2] in self.occupied: stdscr.addch(height-2,width/2,curses.ACS_DARROW,curses.color_pair(3))
        elif self.write==True: stdscr.addch(height-2,width/2,curses.ACS_DARROW,curses.color_pair(2))
      if verse[2]!='0':
        if verse in self.trail.keys() and self.trail[verse]==3: stdscr.addch(height/2,2,curses.ACS_LARROW)
        elif self.adjacents[3] in self.occupied: stdscr.addch(height/2,2,curses.ACS_LARROW,curses.color_pair(3))
        elif self.write==True: stdscr.addch(height/2,2,curses.ACS_LARROW,curses.color_pair(3))
    else:
      with open('/'.join(['data',verse[:verse.index(':')],verse[verse.index(':')+1:]])) as choice: script=choice.readlines()
      self.reset(len(script)+7,max(len(verse),len(max(script,key=len)))+3)
      self.occupied=sorted([':'.join([verse[:verse.index(':')],files]) for files in os.listdir('/'.join(['data',verse[:verse.index(':')]])) if files!='scene'])
      if self.occupied.index(verse)==0: prev=' '
      else: prev=self.occupied[self.occupied.index(verse)-1]
      try: adv=self.occupied[self.occupied.index(verse)+1]
      except IndexError: adv=' '
      self.adjacents=[prev,' ',adv,' ']
      if m.adjacents[0] in m.occupied: stdscr.addch(2,width/2,curses.ACS_UARROW)
      if m.adjacents[2] in m.occupied: stdscr.addch(height-2,width/2,curses.ACS_DARROW)
    stdscr.refresh()
    self.textarea.addstr(1,1,verse[:verse.index(':')+1],curses.color_pair(2))
    self.links.append([1,1,verse[:verse.index(':')+1]])
    self.textarea.addstr(1,6,verse[verse.index(':')+1:],curses.color_pair(1))
    self.textarea.hline(2,0,curses.ACS_HLINE,self.w-1)
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
          else: self.textarea.addstr(y,x,w,curses.color_pair(1))
          x+=len(w)
        y+=1
    with open('log','w') as log: log.write('\n'.join([verse,str(self.trail)]))
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
  curses.init_color(1,1000,1000,1000)
  curses.init_pair(1,1,0) # base
  curses.init_color(3,1000,106,255)
  curses.init_pair(2,3,0) # link
  curses.init_color(4,0,953,396)
  curses.init_pair(3,4,0) # selection
  curses.init_color(5,275,39,1000)
  curses.init_pair(4,5,0) # box drawing
  stdscr.bkgd(' ',curses.color_pair(4))
  with open('log') as log: m.load(log.readlines()[0].rstrip())
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
        except IOError:
          if m.write==True: m.revise(target)
      else: m.load(target)
      target=''
    elif k==ord('r') and m.write==True and target!='':
      if target.endswith(':'): m.revise('scene')
      elif ':' not in target:
        m.revise(target)
        target=''
    elif k==ord('s') and m.ypos+height-4<m.h: m.ypos+=1
    elif k==ord('w') and 0<m.ypos: m.ypos-=1
    elif k in kc:
      if m.adjacents[kc.index(k)].endswith(':'):
        m.trail[m.textarea.instr(1,1,4)]=int(kc.index(k))
        with open('log','w') as log: log.write('\n'.join([m.textarea.instr(1,1,4),str(m.trail)]))
        if m.write==True and m.adjacents[kc.index(k)] not in m.occupied: m.revise(m.adjacents[kc.index(k)])
      if m.adjacents[kc.index(k)] in m.occupied: m.load(m.adjacents[kc.index(k)])
  os.system('setterm -cursor on')
curses.wrapper(main)