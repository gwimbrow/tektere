#! /usr/bin/env python
import sys, os, random, curses
stdscr = curses.initscr()
height,width = stdscr.getmaxyx()
class room:
  def __init__(self):
    self.door = ''
    self.current = ''
    self.firstrun = True
    self.specials = []
    for names in os.listdir(sys.path[0]+'/house/'): self.specials.append(names)
    self.reset()
  def reset(self):
    self.ypos,self.xpos = 0,0
    self.script = []
    self.special_list = []
    self.current_selection = []
    self.current_visible = []
    self.count = 0
  def open_room(self,name):
    if self.door != '':
      del self.textarea
      self.reset()
    self.door = name.lower()
    if self.firstrun == True:
      with open('log') as master: self.current = master.readlines()[1].rstrip()
      self.firstrun = False
    else:
      with open('transcript') as opened: transcript = opened.readlines()
      unopened = []
      for names in os.listdir(sys.path[0]+'/house/'+self.door):
        if str(names+'\n') not in transcript: unopened.append(names)
      if len(unopened) != 0: self.current = random.choice(unopened)
      else:
        self.door = 'epilogue'
        self.current = 'end'
    with open('transcript','a') as opened: opened.write(self.current+'\n')
    with open(sys.path[0]+'/house/'+self.door+'/'+self.current) as choice: self.script = choice.readlines()
    th = len(self.script)+2
    tw = max(len(self.current),len(max(self.script,key=len)))
    self.textarea = curses.newpad(th,tw)
    y,x = 0,0
    for i in range(len(self.script)+1):
      if i < len(self.script): words = self.script[i].rstrip().split(' ')
      else: words = self.current.rstrip().split(' ')
      for j in words:
        if j.lower() in self.specials:
          self.textarea.addstr(y,x,j,curses.color_pair(1))
          self.special_list.append([y,x,j])
        else: self.textarea.addstr(y,x,j)
        x += len(j)+1
      y += 1
      x = 0
    with open('log','w') as master: master.write(self.door+'\n'+self.current)
  def nextspecial(self):
    global height,width
    visible = []
    for j in self.special_list:
      if self.ypos-1 < j[0] < self.ypos+height and self.xpos-1 < j[1] < self.xpos+width: visible.append(j)
    if len(visible) != 0:
      if self.current_visible != visible: self.count = 0
      self.textarea.chgat(visible[self.count][0],visible[self.count][1],len(visible[self.count][2]),curses.color_pair(2))
      if self.current_selection != []:
        self.textarea.chgat(self.current_selection[0],self.current_selection[1],len(self.current_selection[2]),curses.color_pair(1))
      self.current_visible = visible
      self.current_selection = visible[self.count]
      if self.count < len(visible)-1: self.count += 1
      else: self.count = 0
      return self.current_selection[2]
    else: return ''
r = room()
def main(stdscr):
  global height,width
  curses.curs_set(0)
  curses.init_color(1,600,140,80)
  curses.init_color(2,1000,0,0)
  curses.init_pair(1,1,curses.COLOR_BLACK);
  curses.init_pair(2,2,curses.COLOR_BLACK);
  with open('log') as master: r.open_room(master.readlines()[0].rstrip())
  lock = ''
  while True:
    r.textarea.refresh(r.ypos,r.xpos,max(0,(height/2)-(r.textarea.getmaxyx()[0]/2)),max(0,(width/2)-(r.textarea.getmaxyx()[1]/2)),min(height-1,(height/2)+(r.textarea.getmaxyx()[0]/2)),min(width-1,(width/2)+(r.textarea.getmaxyx()[1]/2)))
    k = r.textarea.getch()
    if k == ord('q'): break
    elif k == ord('\t'): lock = r.nextspecial()
    elif k == ord('e') and lock != '': r.open_room(lock)
    elif k == ord('s') and r.ypos+height < r.textarea.getmaxyx()[0]: r.ypos += 1
    elif k == ord('w') and 0 < r.ypos: r.ypos -= 1
    elif k == ord('d') and r.xpos+width < r.textarea.getmaxyx()[1]: r.xpos += 1
    elif k == ord('a') and 0 < r.xpos: r.xpos -= 1
  stdscr.clear()
  stdscr.refresh()
  curses.curs_set(1)
curses.wrapper(main)