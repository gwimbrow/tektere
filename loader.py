#! /usr/bin/env python
import sys, os, random, curses
stdscr = curses.initscr()
height,width = stdscr.getmaxyx()
ypos,xpos = 0,0
class room:
  def __init__(self):
    self.door = ''
    self.current = ''
    self.firstrun = True
    self.reset()
  def reset(self):
    self.script = []
    self.special_list = []
    self.current_selection = []
    self.current_visible = []
    self.count = 0
    stdscr.clear()
  def open_room(self,name):
    global ypos,xpos,house
    if self.door != '':
      log = open(sys.path[0]+'/house/'+self.door+'/'+self.current,'w')
      log.write(str(ypos)+','+str(xpos)+'\n')
      for j in range(1,len(self.script)): log.write(self.script[j])
      log.close()
      del self.textarea
      self.reset()
    self.door = name.lower()
    if self.firstrun == True:
      master = open('log')
      self.current = master.readlines()[1]
      master.close()
      self.firstrun = False
    else: self.current = random.choice(os.listdir(sys.path[0]+'/house/'+self.door))
    stdscr.addstr(1,(width/2)-(len(self.current)/2),self.current)
    stdscr.hline(2,0,curses.ACS_HLINE,width)
    stdscr.refresh()
    choice = open(sys.path[0]+'/house/'+self.door+'/'+self.current)
    self.script = choice.readlines()
    choice.close()
    coords = self.script[0].split(',')
    ypos,xpos = int(coords[0]),int(coords[1])
    size = self.script[1].split(',')
    self.textarea = curses.newpad(int(size[0]),int(size[1]))
    specials = []
    for names in os.listdir(sys.path[0]+'/house/'): specials.append(names)
    for i in range(2,len(self.script)):
      if self.script[i].startswith('{'):
        line = self.script[i].split('}')
        lcoords = line[0].replace('{','').split(',')
        y,x = int(lcoords[0]),int(lcoords[1])
        words = line[1].rstrip().split(' ')
      else: words = self.script[i].rstrip().split(' ')
      for j in words:
        if j.lower() in specials:
          self.textarea.addstr(y,x,j,curses.color_pair(1))
          self.special_list.append([y,x,j])
        else: self.textarea.addstr(y,x,j)
        x += len(j)+1
      y += 1
      x = int(lcoords[1])
    master = open('log','w')
    master.write(self.door+'\n'+self.current)
    master.close()
  def nextspecial(self):
    global ypos,xpos,height,width
    visible = []
    for j in self.special_list:
      if ypos-1 < j[0] < ypos+(height-3) and xpos-1 < j[1] < xpos+width: visible.append(j)
    if len(visible) != 0:
      if self.current_visible != visible: self.count = 0
      if len(self.current_selection) != 0:
        self.textarea.chgat(self.current_selection[0],self.current_selection[1],len(self.current_selection[2]),curses.color_pair(1))
      self.textarea.chgat(visible[self.count][0],visible[self.count][1],len(visible[self.count][2]),curses.color_pair(2))
      self.current_visible = visible
      self.current_selection = visible[self.count]
      if self.count < len(visible)-1: self.count += 1
      else: self.count = 0
      return visible[self.count][2]
    else: return ''
r = room()
def main(stdscr):
  global ypos,xpos,height,width
  curses.curs_set(0)
  curses.init_color(1,600,140,80)
  curses.init_color(2,1000,0,0)
  curses.init_pair(1,1,curses.COLOR_BLACK);
  curses.init_pair(2,2,curses.COLOR_BLACK);
  master = open('log')
  r.open_room(master.readlines()[0].rstrip())
  master.close()
  lock = ''
  while True:
    r.textarea.refresh(ypos,xpos,3,0,height-1,width-1)
    k = r.textarea.getch()
    if k == ord('q'): break
    elif k == ord('\t'): lock = r.nextspecial()
    elif k == ord('e') and lock != '': r.open_room(lock)
    elif k == ord('s') and ypos+height < r.textarea.getmaxyx()[0]: ypos += 1
    elif k == ord('w') and 0 < ypos: ypos -= 1
    elif k == ord('d') and xpos+width < r.textarea.getmaxyx()[1]: xpos += 1
    elif k == ord('a') and 0 < xpos: xpos -= 1
  stdscr.clear()
  stdscr.refresh()
  log = open(sys.path[0]+'/house/'+r.door+'/'+r.current,'w')
  log.write(str(ypos)+','+str(xpos)+'\n')
  for j in range(1,len(r.script)): log.write(r.script[j])
  log.close()
  curses.curs_set(1)
curses.wrapper(main)