#! /usr/bin/env python
import sys
import os
import re
import curses
stdscr = curses.initscr()
height,width = stdscr.getmaxyx()
ypos,xpos = 0,0
run = False
class room:
  def __init__(self):
    self.door = ''
    self.current = ''
    self.script = []
    self.special_list = []
    self.reset()
  def reset(self):
    self.script[:] = []
    self.special_list[:] = []
    self.old_selection = ''
    self.num_visible = ''
    self.count = 0
    stdscr.clear()
  def open_room(self,name):
    global run,ypos,xpos,old_selection
    run = False
    if self.door != '':
      log = open(sys.path[0]+'/house/'+self.door+'/'+self.current,'w')
      log.write(str(ypos)+','+str(xpos)+'\n')
      for j in range(1,len(self.script)): log.write(self.script[j])
      log.close()
      del self.textarea
      self.reset()
    self.door = name
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
        if j in specials:
          self.textarea.addstr(y,x,j,curses.color_pair(1))
          self.special_list.append(str(y)+','+str(x)+'/'+j)
        else: self.textarea.addstr(y,x,j)
        x += len(j)+1
    run = True
  def nextspecial(self):
    global ypos,xpos,height,width
    visible = []
    for j in self.special_list:
      potential = j.split('/')
      potential_coords = potential[0].split(',')
      if ypos-1 < int(potential_coords[0]) < ypos+height and xpos-1 < int(potential_coords[1]) < xpos+width: visible.append(j)
    if len(visible) > 0:
      if self.count > len(visible)-1 or self.num_visible != 0 and self.num_visible != len(visible): self.count = 0
      self.num_visible = len(visible)
      if self.old_selection != '':
        old_selected = self.old_selection.split('/')
        old_coords = old_selected[0].split(',')
        self.textarea.chgat(int(old_coords[0]),int(old_coords[1]),len(old_selected[1]),curses.color_pair(1))
        if self.old_selection == visible[self.count]: self.count += 1
      self.old_selection = visible[self.count]
      selected = visible[self.count].split('/')
      scoords = selected[0].split(',')
      self.textarea.chgat(int(scoords[0]),int(scoords[1]),len(selected[1]),curses.color_pair(4))
      if self.count < len(visible)-1: self.count += 1
      else: self.count = 0
      return selected[1]
    return ''
r = room()
def main(stdscr):
  global run,ypos,xpos,height,width
  curses.curs_set(0)
  curses.use_default_colors()
  for j in range(0, curses.COLORS): curses.init_pair(j,j,-1);
  r.open_room('room')
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
  log = open(sys.path[0]+'/house/'+r.door+'/'+r.current,'w')
  log.write(str(ypos)+','+str(xpos)+'\n')
  for j in range(1,len(r.script)): log.write(r.script[j])
  log.close()
  curses.curs_set(1)
curses.wrapper(main)