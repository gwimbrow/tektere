#! /usr/bin/env python
import sys,os,ast,curses

# use psf2txt <your font>.psf <your font>.txt
# to generate an editable bitmap font. Save using
# txt2psf <your font>.txt <your font>.psf
#
# the file named <your font> contains settings for
# colors and the animation sequence represented by
# a string of alpha-numeric characters, edited
# versions of which will be displayed consecutively
# on the screen, in the pattern described within
# the entry file loaded as sys.argv[1]
#
# important: use 'sudo dpkg-reconfigure console-setup'
# and 'setupcon' to set and restore the default tty font

stdscr = curses.initscr()
height, width = stdscr.getmaxyx()

class carto:

  def load(self):

    with open(sys.argv[1]) as choice:
      font, rate, bg, fg = ast.literal_eval(choice.readline())
      self.script = choice.readlines()
      for i in range(len(self.script)):
        self.script[i] = list(self.script[i].rstrip())

    self.seq = map(chr, range(97, 123))
    self.h = len(self.script)
    self.w = len(self.script[0])
    self.area = curses.newpad(self.h, self.w)
    self.area.timeout(rate)

    curses.init_color(1, bg[0], bg[1], bg[2])
    curses.init_color(2, fg[0], fg[1], fg[2])
    curses.init_pair(2, 1, 2)
    os.system('setfont ' + font + '.psf')

  def update(self):

    for y in range(self.h - 1):
      for x in range(len(self.script[y]) - 1):
        index = self.seq.index(self.script[y][x])
        self.area.addstr(y, x, self.script[y][x], curses.color_pair(2))
        self.script[y][x] = self.seq[index + 1] if index < len(self.seq) - 1 else self.seq[0]

    a = (self.h - height) / 2
    b = (self.w - width) / 2
    c = max(0, (height - self.h) / 2)
    d = max(0, (width - self.w) / 2)
    e = min(height, (height + self.h) / 2) - 1
    f = min(width ,(width + self.w) / 2) - 1
    self.area.refresh(a, b, c, d, e, f)

m = carto()

def main(stdscr):

  curses.curs_set(0)
  m.load()

  while True:
    m.update()
    k = m.area.getch()
    if k == ord('q'): break

  curses.curs_set(1)
  os.system('setupcon')

curses.wrapper(main)