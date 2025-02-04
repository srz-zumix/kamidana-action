# for windows
import sys

if sys.platform == "win32":
  import io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, newline='')
