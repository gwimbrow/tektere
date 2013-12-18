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
  def open_room(self,name):
    global run,ypos,xpos
    run = False
    if name != self.door and self.door != '':
      log = open(sys.path[0]+'/house/'+self.door+'/'+self.current,'w')
      log.write(str(ypos)+','+str(xpos)+'\n')
      for j in range(1,len(self.script)): log.write(self.script[j])
      log.close()
      del self.textarea
      stdscr.clear()
      stdscr.refresh()
    self.door = name
    exec 'from house.'+self.door+'.config import chooser'
    self.current = chooser()
    choice = open(sys.path[0]+'/house/'+self.door+'/'+self.current)
    self.script = choice.readlines()
    choice.close()
    coords = self.script[0].split(',')
    ypos,xpos = int(coords[0]),int(coords[1])
    size = self.script[1].split(',')
    self.textarea = curses.newpad(int(size[0]),int(size[1]))
    for i in range(2,len(self.script)):
      line = self.script[i].split('/')
      lcoords = line[0].split(',')
      y,x = int(lcoords[0]),int(lcoords[1])
      words = line[1].rstrip().split(' ')
      house = os.listdir(sys.path[0]+'/house/')
      specials = []
      for names in house:
        specials.append(names)
      for j in words:
        if j in specials:
          self.textarea.addstr(y,x,j,curses.A_REVERSE)
        else: self.textarea.addstr(y,x,j,curses.A_NORMAL)
        x += len(j)+1
    run = True
r = room()
def main(stdscr):
  global run,ypos,xpos,height,width
  curses.curs_set(0)
  r.open_room('room')
  while True:
    r.textarea.refresh(ypos,xpos,0,0,height-1,width-1)
    k = r.textarea.getch()
    if k == ord('q'): break
    elif k == ord('\t'): r.open_room('line')
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