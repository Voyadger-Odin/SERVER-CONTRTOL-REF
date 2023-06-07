
import math


def getNameHash(name):
    startFileName = name.split('/')
    startFileName = startFileName[len(startFileName) - 1].split('.')
    startFileName = startFileName[0]

    name = name.replace('/', '__').replace('\\', '__')

    return f'{startFileName}-{name}.txt'



def MemorySizeFormat(size):
    if size == 0:
        return '0 б'
    pwr = math.floor(math.log(size, 1024))
    suff = ['б', 'кб', 'мб', 'гб', 'тб', 'пб']
    if size > 1024 ** (len(suff) - 1):
        return "не знаю как назвать такое число :)"
    return f"{size / 1024 ** pwr:.0f} {suff[pwr]}"