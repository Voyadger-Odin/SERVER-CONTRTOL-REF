import re

class out():

    def __init__(self, path_cmd, cmdfilename):
        self.cmdfilename = cmdfilename
        self.file = None
        self.cmd_path = f'{path_cmd}/console'
        self.name = f'{self.cmd_path}/{cmdfilename}'
        self.mode = 'a'

        self.lineWrite = ''
        self.writeCom = 0
        self.cursorPosition = {'x': 0, 'y': 0}

    def __del__(self):
        self.file.close()


    def MatchCommand(self, data, command):
        r = re.match(command, data)
        return r

    def getOffset(self, f):
        offset = 0
        f.seek(0)
        lines = f.read().split('\n')

        # Смещение по Y
        for l in lines[:self.cursorPosition['y']]:
            offset += len(l.encode())
        offset += self.cursorPosition['y']

        # Смещение по X
        offset += len(lines[self.cursorPosition['y']][:self.cursorPosition['x']].encode())
        return offset

    def CursorAddSpaces(self, f):
        f.seek(0)
        lines = f.read().split('\n')

        spacesAdd = self.cursorPosition['x'] - len(lines[self.cursorPosition['y']]) + 1
        if (spacesAdd > 0):
            offset = self.getOffset(f)
            f.seek(offset)
            dataAfterCursor = f.read()
            f.seek(offset)
            f.write(' ' * spacesAdd)
            f.truncate()
            f.seek(0, 2)
            f.write(dataAfterCursor)

    def CursorAddLines(self, f):
        f.seek(0)
        lines = f.read().split('\n')

        linesAdd = self.cursorPosition['y'] - len(lines) + 1
        if (linesAdd > 0):
            f.seek(0, 2)
            f.write('\n' * linesAdd)

    def write(self, c):

        self.file = open(self.name, self.mode)
        self.file.close()

        commands = {
            'cursorMove': '^\x1b\[?(\d+)?;?(\d+)?([ABCDH])?$',
            'consoleColor': '^\x1b\[([01];)?(\d+)?(m)?$',
            '\r': '^\r$',
            '\n': '^\n$',
            '\t': '^\t$'
        }
        '''
        writeCom = 0 - обычная строка
        writeCom = 1 - запись комманды
        writeCom = 2 - команда выполнена
        
python3 starter.py
        '''
        with open(self.name, 'r+') as f:
            self.lineWrite += c
            for com in commands:
                self.writeCom = 0
                match = re.match(commands[com], self.lineWrite)  # self.MatchCommand(self.lineWrite, com)
                if not(match is None):
                    self.writeCom = 1

                    if not(match is None):
                        groups = match.groups()
                        self.writeCom = 1


                        # Выполнить комманду


                        if (com == 'consoleColor'):
                            if len(groups) >= 3:
                                if (groups[-1] == 'm'):
                                    self.lineWrite = ''
                                    self.writeCom = 0

                        # Движение курсора
                        if (com == 'cursorMove'):
                            dir = groups[-1]
                            # UP
                            if (dir == 'A'):
                                self.cursorPosition['y'] -= int(groups[0])
                            # DOWN
                            if (dir == 'B'):
                                self.cursorPosition['y'] += int(groups[0])
                            # FORWARD
                            if (dir == 'C'):
                                self.cursorPosition['x'] += int(groups[0])
                            # BACK
                            if (dir == 'D'):
                                self.cursorPosition['x'] -= int(groups[0])
                            # POS
                            if (dir == 'H'):
                                self.cursorPosition['y'] = int(groups[0])
                                if not(groups[1] is None):
                                    self.cursorPosition['x'] = int(groups[1])



                            # -------------------
                            if not(dir is None) and dir in 'ABCDH':
                                self.lineWrite = ''
                                self.writeCom = 2

                            break  # Завершаем перебор комманд


                        # Перенос каретки в начало строки
                        if (com == '\r'):
                            self.cursorPosition['x'] = 0

                            # -------------------
                            self.lineWrite = ''
                            self.writeCom = 2
                            break  # Завершаем перебор комманд

                        # Перенос на новую строку
                        if (com == '\n'):
                            self.cursorPosition['y'] += 1
                            self.cursorPosition['x'] = 0

                            # -------------------
                            self.lineWrite = ''
                            self.writeCom = 2
                            break  # Завершаем перебор комманд
                        # Табуляция
                        if (com == '\t'):
                            self.cursorPosition['x'] += 8 - self.cursorPosition['x'] % 8

                            # -------------------
                            self.lineWrite = ''
                            self.writeCom = 2
                            break  # Завершаем перебор комманд

            # Если комманда выполнена
            if self.writeCom == 2:
                self.writeCom = 0

            # Если обычная строка
            elif self.writeCom == 0:
                self.CursorAddLines(f)
                self.CursorAddSpaces(f)

                # Запись в файл
                offset = self.getOffset(f)

                f.seek(offset)
                dataAfterCursor = f.read()
                f.seek(offset)
                f.truncate()

                f.seek(offset)
                f.write(self.lineWrite)

                f.write(dataAfterCursor[1:])
                # --------------

                self.cursorPosition['x'] += 1
                self.lineWrite = ''

    def flush(self):
        self.file.flush()