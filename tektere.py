#! /usr/bin/env python
import sys,os,ast,curses
stdscr=curses.initscr()
height,width=stdscr.getmaxyx()
class carto:
  def load(self):
    with open(sys.argv[1]) as choice:
      rate,self.h,self.w,font=ast.literal_eval(choice.readline())
      self.script=choice.readlines()
    os.system('setfont '+font+'.psf')
    with open(font) as defs:
      colors=ast.literal_eval(defs.readline()) # a list of two color tuples
      self.seqs=defs.readlines() # lists of animation sequences
    for c in range(len(colors)):
      r,g,b=colors[c]
      curses.init_color(c+1,r,g,b)
      curses.init_pair(c+1,c,c+1)
    self.area=curses.newpad(self.h+1,self.w+1)
    self.area.timeout(rate)
  def update(self):
    for i in range(1,self.h):
      line=list(self.script[i].rstrip())
      for l in range(len(line)):
        self.area.addstr(i-1,l,line[l],curses.color_pair(2))
        for cell in [g.rstrip() for g in self.seqs if line[l] in g]:
          if cell.index(line[l])<len(cell)-1: n=cell[cell.index(line[l])+1]
          else: n=cell[0]
          line[l]=n
      self.script[i]=''.join(line)
    self.area.refresh((self.h-height)/2,(self.w-width)/2,max(0,(height-self.h)/2),max(0,(width-self.w)/2),min(height,(height+self.h)/2)-1,min(width,(width+self.w)/2)-1)
m = carto()
def main(stdscr):
  curses.curs_set(0)
  m.load()
  while True:
    m.update()
    k=m.area.getch()
    if k==ord('q'): break
  # Replace with early function to navigate through files on a cartesian plane. The files themselves are named as coordinate pairs: y.x in this case
  curses.curs_set(1)
curses.wrapper(main)