#! /usr/bin/env python
import os,ast,math,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
def rect(t,r,b,l,g,c):
  for y in range(max(0,int(t)),min(height,int(height-b))):
    for x in range(max(0,int(l)),min(width,int(width-r))):
      stdscr.insch(y,x,g,curses.color_pair(c))
def main(stdscr):
  curses.curs_set(0)
  fc=0
  with open('source') as choice: script=choice.readlines()
  config=ast.literal_eval(script[0])
  rate,duration=config[0]
  stdscr.timeout(rate)
  for j in range(1,len(config)):
    r,g,b=config[j]
    curses.init_color(j,r,g,b)
    curses.init_pair(j,j,0)
  while True:
    stdscr.erase()
    for i in script[1:]:
      try: exec(i)
      except Exception: pass
    if fc<duration: fc+=1
    else: fc=0
    k=stdscr.getch()
    if k==ord('q'): break
  curses.curs_set(1)
curses.wrapper(main)
