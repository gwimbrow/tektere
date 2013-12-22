#! /usr/bin/env python
import sys
import os
import re
import curses
stdscr = curses.initscr()
height,width = stdscr.getmaxyx()
ypos,xpos = 0,0
class room:
  def __init__(self):
    self.door = ''
    self.current = ''
    self.reset()
  def reset(self):
    self.script = []
    self.special_list = []
    self.old_selection = []
    self.num_visible = ''
    self.count = 0
    stdscr.clear()
  def open_room(self,name):
    global ypos,xpos
    if self.door != '':
      log = open(sys.path[0]+'/house/'+self.door+'/'+self.current,'w')
      log.write(str(ypos)+','+str(xpos)+'\n')
      for j in range(1,len(self.script)): log.write(self.script[j])
      log.close()
      del self.textarea
      self.reset()
    self.door = name.lower()
    exec 'from house.'+self.door+'.config import chooser'
    self.current = chooser()
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
    house = os.listdir(sys.path[0]+'/house/')
    specials = []
    for names in house: specials.append(names)
    for i in range(2,len(self.script)):
      line = self.script[i].split('/')
      lcoords = line[0].split(',')
      y,x = int(lcoords[0]),int(lcoords[1])
      words = line[1].rstrip().split(' ')
      for j in words:
        if j.lower() in specials:
          self.textarea.addstr(y,x,j,curses.color_pair(1))
          self.special_list.append([y,x,j])
        else: self.textarea.addstr(y,x,j)
        x += len(j)+1
  def nextspecial(self):
    global ypos,xpos,height,width
    visible = []
    for j in self.special_list:
      if ypos-1 < j[0] < ypos+height and xpos-1 < j[1] < xpos+width: visible.append(j)
    if len(visible) != 0:
      if self.count > len(visible)-1 or self.num_visible != len(visible): self.count = 0
      self.num_visible = len(visible)
      if len(self.old_selection) != 0:
        self.textarea.chgat(self.old_selection[0],self.old_selection[1],len(self.old_selection[2]),curses.color_pair(1))
        if self.old_selection == visible[self.count] and 0 < len(visible)-1: self.count += 1
      self.old_selection = visible[self.count]
      selected = visible[self.count][2]
      self.textarea.chgat(visible[self.count][0],visible[self.count][1],len(selected),curses.color_pair(2))
      if self.count < len(visible)-1: self.count += 1
      else: self.count = 0
      return selected
    return ''
r = room()
def main(stdscr):
  global ypos,xpos,height,width
  lock = ''
  curses.curs_set(0)
  curses.init_color(1,500,400,800)
  curses.init_color(2,150,100,400)
  curses.init_color(3,700,400,1000)
  curses.init_pair(1,1,curses.COLOR_BLACK);
  curses.init_pair(2,2,3);
  master = open('master')
  r.open_room(master.read().rstrip())
  master.close()
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
  master = open('master','w')
  master.write(r.door)
  master.close()
  curses.curs_set(1)
curses.wrapper(main)