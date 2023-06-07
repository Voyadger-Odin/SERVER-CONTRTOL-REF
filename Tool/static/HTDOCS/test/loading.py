import time

'''
from alive_progress.styles import showtime, Show

showtime(Show.BARS)
'''

'''
from progress.bar import Bar

print('test')
with Bar('Processing', max=20) as bar:
    for i in range(20):
        # Do some work
        #print('+')
        time.sleep(.1)
        bar.next()
'''


print('TEST')

size = 60
for i in range(size+1):
	time.sleep(0.05)
	print(f'\rLoading: [{"="*i}{">" if (i<size) else "="}{" "*(size-i)}] {int((i/size*100))}%', end='')

print()
print('Loading compleated')


'''
frames = ['\\', '|', '/', '-']

frame = 0
while True:

	print('\r', f'Loading: {frames[frame]}', end='')

	frame += 1
	if (frame >= len(frames)):
		frame = 0
	time.sleep(0.2)
'''
