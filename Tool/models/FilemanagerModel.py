
import flask
import os
import time

from Tool import CONSTANTS
from Tool.Mechanics import Functions



def dayFormat(day):
    if day < 10:
        return f'0{day}'
    return f'{day}'

def index(request=None, user=None):
    GETPath = request.args.get('path')
    if (GETPath is None) or (GETPath == '/') or ('..' in GETPath):
        return flask.redirect('?path=')

    GETPath = f'{GETPath}'.replace('//', '/')

    dirname = 'Tool/static/HTDOCS'

    dirname = f'{os.getcwd()}/{dirname}/{GETPath}'

    #pathview_split = dirname.split('/')
    dirfiles = os.listdir(dirname)
    fullpaths = map(lambda name: os.path.join(dirname, name), dirfiles)



    dirs = []
    files = []
    files_result = []

    for file in fullpaths:
        # Папка
        if os.path.isdir(file):
            dirs.append(file)
        else:
            files.append(file)

    fullpaths = dirs + files

    markdown = False
    markdownText = ''

    for file in fullpaths:
        file_createdTime = time.localtime(os.path.getctime(file))
        file_createdTime_str = f'{dayFormat(file_createdTime.tm_mday)}.{dayFormat(file_createdTime.tm_mon)}.{file_createdTime.tm_year}'

        file_path = GETPath
        file_name = file.split('/')[-1]
        file_size = None
        file_type = None
        file_type_obj = None
        file_icon = None
        file_dbaction = None
        file_actions = []

        # Папка
        if os.path.isdir(file):
            file_size_c = len(os.listdir(dirname + "/" + file_name))
            file_size_t = ''
            if (file_size_c == 1):
                file_size_t = 'объект'
            elif (2 <= file_size_c <=4):
                file_size_t = 'объекта'
            elif (5 <= file_size_c) or (file_size_c == 0):
                file_size_t = 'объектов'
            file_size = f'{file_size_c} {file_size_t}'
            file_type = 'folder'
            file_type_obj = 'folder'
            file_icon = CONSTANTS.icons[file_type]
            file_dbaction = f'folderOpen("{file_name}")'

            file_actions = [
                {
                    'name': 'Перейти',
                    'action': f'folderOpen("{file_name}")'
                }
            ]

        # Файл
        if os.path.isfile(file):
            file_size = Functions.MemorySizeFormat(os.path.getsize(file))
            file_type = file.split('.')[-1]
            file_type_obj = 'file'
            file_icon = CONSTANTS.icons[file_type] if (file_type in CONSTANTS.icons) else CONSTANTS.icons['']

            if file_name == 'README.md':
                file_icon = CONSTANTS.icons[file_name]

            file_dbaction = f'openFile("{file_name}")'

            # Картинка
            if (file_type in CONSTANTS.types_img):
                file_type_obj = 'img'
                file_dbaction = None

            # Архив
            if (file_type in CONSTANTS.types_arc):
                if user['role'] in ('admin', 'developer',):
                    file_dbaction = None
                    file_actions = [
                        {
                            'name': 'Разархивировать',
                            'action': f'uparchiv("{file_name}")'
                        }
                    ]

            # Текстовый файл
            if not(file_type in CONSTANTS.types_img) and not(file_type in CONSTANTS.types_arc):
                file_actions = [
                    {
                        'name': 'Редактировать',
                        'action': f'openFile("{file_name}")'
                    }
                ]

            # Скрипт
            if (file_type == 'py'):
                file_actions = [
                    {
                        'name': 'Запустить',
                        'action': f'scriptStart("{file_name}")'
                    }
                ]

            # База данных (sqlite)
            if (file_type == 'sqlite'):
                file_dbaction = f'openDataBase("{file_name}")'
                file_actions = [
                    {
                        'name': 'Открыть таблицу',
                        'action': f'openDataBase("{file_name}")'
                    }
                ]

            # Аудио (mp3)
            if (file_type == 'mp3'):
                file_dbaction = f'openAudio("{file_name}")'
                file_actions = [
                    {
                        'name': 'Открыть аудио',
                        'action': f'openAudio("{file_name}")'
                    }
                ]

            # MarkDown
            if (file_name == 'README.md'):
                with open(file, 'r') as f:
                    markdownText = ''
                    for line in f.read().split('\n'):
                        line = line.replace('\'', '\\\'')

                        if markdownText != '':
                            markdownText += '+\n'
                        markdownText += f'\'{line}\\n\''

                    markdown = True

        files_result.append({
            'path': file_path,
            'name': file.split('/')[-1],
            'file_createdTime': file_createdTime_str,
            'size': file_size,
            'type': file_type,
            'type_obj': file_type_obj,
            'icon': file_icon,
            'dbaction': file_dbaction,
            'actions': file_actions,
        })


    breadcrumb = []

    breadcrumb_list = GETPath.split('/')
    breadcrumb_path = ''
    for i in range(len(breadcrumb_list)):
        if (i==0):
            breadcrumb.append({
                'name': 'HTDOCS',
                'active': i == (len(breadcrumb_list) - 1),
                'path': breadcrumb_path
            })
            continue

        breadcrumb_path += f'/{breadcrumb_list[i]}'
        breadcrumb.append({
            'name': breadcrumb_list[i],
            'active': i == (len(breadcrumb_list) - 1),
            'path': breadcrumb_path,
        })

    return flask.render_template(
        '/pages/filemanager.html',
        user=user,
        page='filemanager',
        title='filemanager',
        files=files_result,
        breadcrumb=breadcrumb,

        markdown=markdown,
        markdownText=markdownText
    )