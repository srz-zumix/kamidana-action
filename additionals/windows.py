# for windows
import sys

if sys.platform == "win32":
  import os, msvcrt
  msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY) if os.name == 'nt':
  os.linesep = '\n'
