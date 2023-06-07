import colorama as col
import time

effect = [col.Fore.YELLOW, col.Style.BRIGHT, col.Cursor.UP()]
line_effect = ''.join(effect)

#print(effect)
#print()
#print(f'{line_effect}TEXT')

#print('123\n123\x1b[1A')

itters = 30
for i in range(itters + 1):
    print('|', '=' * (i + 1), ' ' * (itters - i), f'| {int(i / itters * 100)}%', sep='', end='\n')
    print('|', '=' * (i * 2 + 1), ' ' * (itters * 2 - i * 2), f'| {int(i / itters * 100)}%', sep='', end='\n')
    print('\x1b[1A' * 2, end='')
    time.sleep(.1)

print('\n\n')
