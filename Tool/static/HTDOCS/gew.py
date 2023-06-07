import time

i = 0
while True:
  print(f'line - {i + 1}')
  i += 1
  if (i >= 4):
    break
  time.sleep(1)