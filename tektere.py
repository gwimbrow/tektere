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

      rate, font = ast.literal_eval(choice.readline())
      self.script=choice.readlines()
      self.h = len(self.script)
      self.w = len(self.script[0])

    os.system('setfont ' + font + '.psf')

    with open(font) as defs:

      colors = ast.literal_eval(defs.readline()) # a list of two color tuples
      self.seqs = defs.readlines() # lists of animation sequences

    for c in range(len(colors)):

      r, g, b = colors[c]
      curses.init_color(c + 1, r, g, b)
      curses.init_pair(c + 1, c, c + 1)

    self.area = curses.newpad(self.h, self.w)
    self.area.timeout(rate)

  def update(self):

    for i in range(1, self.h):

      line = list(self.script[i].rstrip())

      for l in range(len(line)):

        self.area.addstr(i - 1, l, line[l], curses.color_pair(2))

        for cell in [g.rstrip() for g in self.seqs if line[l] in g]:

          if cell.index(line[l]) < len(cell) - 1: n = cell[cell.index(line[l]) + 1]
          else: n = cell[0]

          line[l] = n

      self.script[i] = ''.join(line)

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