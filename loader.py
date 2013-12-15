#! /usr/bin/env python

import sys
import os
import re
import curses

stdscr = curses.initscr()
height,width = stdscr.getmaxyx()
rooms = {}

def open_room(r,old_r):

  if old_r != '':
    log = open(sys.path[0]+'/house/'+old_r+'/map','w')
    log.write(str(ypos)+','+str(xpos)+'\n')
    for j in range(1,len(script)):
      log.write(script[j])
    log.close()
    del textarea

  old_r = r
  
  config = open(sys.path[0]+'/house/'+r+'/map')
  script = config.readlines()
  config.close()
  
  coords = script[0].split(',')
  ypos,xpos = int(coords[0]),int(coords[1])

  psize = script[1].split(',')
  h,w = int(psize[0]),int(psize[1])
  
  textarea = curses.newpad(h,w)

  for i in range(2,len(script)):
    line = script[i].split('/')
    y,x = int(line[0].split(',')[0]),int(line[0].split(',')[1])
    house = os.listdir(sys.path[0]+'/house/')
    words = line[1].split(' ')
    specials = []
    for j in words:
      for names in house:
        if str(names) == j: specials.append(str(names))
    fragments = re.split("|".join(specials),line[1])
    for j in range(max(len(fragments),len(specials))):
      if j < len(fragments):
        textarea.addstr(y,x,fragments[j],curses.A_NORMAL)
        x += len(fragments[j])
      if j < len(specials):
        textarea.addstr(y,x,specials[j],curses.A_REVERSE)
        key = str(y)+','+str(x)+','+str(x + len(specials[j]))
        rooms[key] = specials[j]
        x += len(specials[j])
  
  while True:
    textarea.refresh(ypos,xpos,0,0,height-1,width-1)
    k = textarea.getch()
    if k == ord('q'): break
    elif k == curses.KEY_MOUSE: print "mouseclick"
    elif k == ord('w') and ypos > 0: ypos -= 1
    elif k == ord('s') and ypos < h-height: ypos += 1
    elif k == ord('a') and xpos > 0: xpos -= 1
    elif k == ord('d') and xpos < w-width: xpos += 1

    log = open(sys.path[0]+'/house/'+r+'/map','w')
    log.write(str(ypos)+','+str(xpos)+'\n')
    for j in range(1,len(script)):
      log.write(script[j])
    log.close()

def main(stdscr):
  curses.mousemask(curses.BUTTON1_CLICKED)
  curses.mouseinterval(200)
  open_room('room','')
  
curses.wrapper(main)