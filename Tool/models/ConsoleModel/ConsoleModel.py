import os.path
import sys
import json
import threading
import re

import psutil
import subprocess

from flask import render_template

from Tool.CONSTANTS import *
from Tool.DATABASE import sqlighter
from Tool.Mechanics import Functions

from Tool.models.ConsoleModel.OutClass import  out

RUNProcess = {}




def getConsole(request):
    fullName = request.args.get('fullName')
    cmdfilename = Functions.getNameHash(fullName)
    cmd_path = f'{path_cmd}/console'

    test_file = os.path.exists(f'{cmd_path}/{cmdfilename}')

    data = ''


    if (test_file):
        with open(f'{cmd_path}/{cmdfilename}', 'r') as f:
            data = f.read()

    if not(cmdfilename in RUNProcess):
        os.remove(f'{cmd_path}/{cmdfilename}')
    else:
        print(RUNProcess[cmdfilename].pid)
        p = psutil.Process(pid=RUNProcess[cmdfilename].pid)
        print(Functions.MemorySizeFormat(p.memory_full_info().uss))
        #print(p.io_counters())

    return json.dumps(
        {
            'data': data,
            'meta': {
                'end': not(cmdfilename in RUNProcess)
            }
        }
    )


def cmd(request):
    fullName = request.args.get('fullName')

    startFileName = fullName.split('/')
    startFileName = startFileName[len(startFileName) - 1]
    filePathHash = Functions.getNameHash(fullName)

    if not (sqlighter.has_console(console_path_hash=filePathHash)):
        # sqlighter.add_new_console(console_name=startFileName, console_path=fullName, console_path_hash=filePathHash)
        script = threading.Thread(target=startScript, args=(fullName, filePathHash,))
        script.start()

    path_startFile = f'{path}{fullName}'
    path_startDir = path_startFile.split('/')[:-1]
    path_startDir = '/'.join(path_startDir)
    endline = f'[[;;;item-Green]{os.getlogin()}@server][[;;;item-White]:][[;;;item-Blue]~{path_startDir}][[;;;item-White]$] '

    return render_template(
        'pages/console.html',
        endline=endline
    )


def startAllConsoles():
    print('start consoles')
    consoles = sqlighter.get_all_console()
    for console in consoles:
        console_path = console[2]
        console_path_hash = console[3]

        script = threading.Thread(target=startScript, args=(console_path, console_path_hash,))
        script.start()


def formatText(data):
    first = data.find('\033')

    data = data.replace('\033[39m', '][[;;;item-Default]')
    data = data.replace('\033[30m', '][[;;;item-Black]')
    data = data.replace('\033[31m', '][[;;;item-Dark-red]')
    data = data.replace('\033[32m', '][[;;;item-Dark-green]')
    data = data.replace('\033[33m', '][[;;;item-Dark-yellow]')
    data = data.replace('\033[34m', '][[;;;item-Dark-blue]')
    data = data.replace('\033[35m', '][[;;;item-Dark-magenta]')
    data = data.replace('\033[36m', '][[;;;item-Dark-cyan]')
    data = data.replace('\033[37m', '][[;;;item-Light-gray]')
    data = data.replace('\033[90m', '][[;;;item-Dark-gray]')
    data = data.replace('\033[91m', '][[;;;item-Red]')
    data = data.replace('\033[92m', '][[;;;item-Green]')
    data = data.replace('\033[93m', '][[;;;item-Orange]')
    data = data.replace('\033[94m', '][[;;;item-Blue]')
    data = data.replace('\033[95m', '][[;;;item-Magenta]')
    data = data.replace('\033[96m', '][[;;;item-Cyan]')
    data = data.replace('\033[97m', '][[;;;item-White]')

    if (first >= 0):
        data = data[:first] + data[first + 1:]
    return data


def stopscript(filePathHash):
    if (sqlighter.has_console(console_path_hash=filePathHash)):
        #p = psutil.Process(pid=RUNProcess[filePathHash].pid)
        #p.kill()
        #RUNProcess[filePathHash].kill()

        RUNProcess[filePathHash].terminate()
        RUNProcess[filePathHash].kill()

        if (filePathHash in RUNProcess):
            RUNProcess.pop(filePathHash)

        sqlighter.close_console(console_path_hash=filePathHash)

    return 'ok'





def startScript(startFile, filePathHash):
    # Полный путь к файлу скрипта
    path_startFile = f'{path}{startFile}'

    path_startDir = path_startFile.split('/')[:-1]
    path_startDir = '/'.join(path_startDir)
    startFileName = path_startFile.split('/')[-1]

    if (filePathHash in RUNProcess):
        return

    com_win = [
        'cmd.exe',
        '/k',
        'cd',
        '/d',
        path_startDir,
        '&',
        'cd',
        '&',
        'python',
        '-u',
        path_startFile
    ]

    '''
    arr = [
        'echo "\033[30m colorful text\033[0m"',
        'echo "\033[31m colorful text\033[0m"',
        'echo "\033[32m colorful text\033[0m"',
        'echo "\033[33m colorful text\033[0m"',
        'echo "\033[34m colorful text\033[0m"',
        'echo "\033[35m colorful text\033[0m"',
        'echo "\033[36m colorful text\033[0m"',
        'echo "\033[37m colorful text\033[0m"',
    ]
    com_lin = '; '.join(arr)
    '''

    out_obj = out(path_cmd, filePathHash)

    com_lin = f'cd {path_startDir}; python3 -u {path_startFile}'
    #com_lin = f'mc'

    print('com_lin', com_lin)

    process = subprocess.Popen(com_lin,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True,
                               pipesize=1024 * 900
                               )

    sqlighter.add_new_console(pid=process.pid, console_name=startFileName, console_path=path_startFile,
                              console_path_hash=filePathHash)

    p = psutil.Process(pid=process.pid)
    print(Functions.MemorySizeFormat(p.memory_full_info().uss))
    RUNProcess.update({filePathHash: process})

    stream_chr_line = b''
    test_encode = True

    while filePathHash in RUNProcess:

        # Для многобайтовых символов
        stream = process.stdout.read(1)
        if stream != '':
            stream_chr_line += stream
        try:
            stream_chr = stream_chr_line.decode('utf-8')
            stream_chr_line = b''
            test_encode = True
        except:
            test_encode = False

        # Запись в файл
        if test_encode:
            if stream_chr != '':
                out_obj.write(stream_chr)

        # Завершение консоли
        if not(process.poll() is None) and stream_chr == '':
            stopscript(filePathHash)



    return 'ok'
