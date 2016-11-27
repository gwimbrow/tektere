# Tektere

Tektere is a program for displaying animated graphics on a TTY terminal. The Python script loads a custom .psf font, which is used to "typeset" an image on the screen.

Invoke the script with a configuration file included in the public repo:

```
python tektere.py test
```

Pressing *q* will terminate the program.

## Creating Custom Fonts

John Elliott's [psftools](http://www.seasip.info/Unix/PSF/) provide a straightforward means of editing TTY display fonts from within a text editor. A "blank" font is included with the repo.

Compile .txt to .psf:

```
txt2psf font.txt font.psf
```

## Scripting Animations

The first line of a configuration script will be evaluated to obtain four values: the name of a font, a framerate, and two colors - foreground and background - as RGB triplets.

In the current iteration, Tektere creates a looping animation from the sequence of font characters spanning (lowercase) a - z, following a pattern described in the remaining lines of a configuration file. The provided one - test - sources the 'test' font, and renders a pattern of characters to the screen. On each tick, the program re-renders the pattern, replacing each character with the next one in the animated sequence.