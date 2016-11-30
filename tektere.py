#! /usr/bin/env python
import sys,os,ast,curses

# use 'psf2txt <your font>.psf <your font>.txt' to generate an editable bitmap font,
# and 'txt2psf <your font>.txt <your font>.psf' to compile a font from a text file.
#
# use 'sudo dpkg-reconfigure console-setup' and 'setupcon' to set and restore the default tty font

stdscr = curses.initscr()
height, width = stdscr.getmaxyx()

class carto:

  def load(self):

    with open(sys.argv[1]) as choice:
      font, start, end, rate, bg, fg = ast.literal_eval(choice.readline())
      self.script = map(lambda x: list(x.rstrip()), choice.readlines())

    self.seq = map(chr, range(start, end + 1))

    self.h = len(self.script)
    self.w = len(max(self.script))

    self.area = curses.newpad(self.h + 1, self.w + 1)
    self.area.timeout(rate)

    curses.init_color(1, bg[0], bg[1], bg[2])
    curses.init_color(2, fg[0], fg[1], fg[2])
    curses.init_pair(2, 1, 2)

    os.system('setfont ' + font + '.psf')

  def update(self):

    for y in range(self.h):

      for x in range(len(self.script[y])):

        try:
          char = self.script[y][x]
          indx = self.seq.index(char) + 1
          self.script[y][x] = self.seq[indx] if indx < len(self.seq) else self.seq[0]
          pair = 2
        except Exception:
          char = ' '
          pair = 1

        self.area.addstr(y, x, char, curses.color_pair(pair))

    self.area.refresh(0, 0, height - self.h, (width - self.w) / 2, height - 1, width - 1)

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