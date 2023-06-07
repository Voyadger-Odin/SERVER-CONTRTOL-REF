from flask import Flask, request, redirect, render_template, session
from Tool.models import api

from Tool.DATABASE import sqlighter

app = Flask(__name__)
app.config['SECRET_KEY'] = '95c844b58eeb12a4377ec6cf924a28e4d951d524'


# Models
from Tool.models import FilemanagerModel, EditorModel, ProcesesModel, StatisticModel, MediaPlayerModel, UsersModel
from Tool.models import ContainersModel
from Tool.models.DataBaseReaderModel import DataBaseReaderModel
from Tool.models.ConsoleModel import ConsoleModel

from Tool.Mechanics import Functions


'''
Главная страница
'''
@app.route('/')
def index():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return render_template('pages/index.html', title='index', session=session, user=user)

'''
Авторизация
'''
@app.route('/login')
def login():
    if 'user' in session:
        return redirect('/')
    return render_template('pages/login.html')

@app.route('/login', methods = ['POST'])
def login_post():
    return UsersModel.Login(request=request)

@app.route('/logout')
def logout():
    return UsersModel.Logout()

'''
Файловый менеджер
'''
@app.route('/filemanager')
def filemanager():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return FilemanagerModel.index(request=request, user=user)

'''
Процессы
'''
@app.route('/proceses')
def proceses():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return ProcesesModel.index(user=user)

'''
Статистика
'''
@app.route('/statistic')
def statistic():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return StatisticModel.index(user=user)


'''
Редактор кода
'''
@app.route('/editor')
def editor():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return EditorModel.editor(request.args, user=user)


'''
Запуск консоли
'''
@app.route('/cmd')
def cmd():
    if not('user' in session):
        return redirect('/login')
    return ConsoleModel.cmd(request)


'''
Запуск консоли
'''
@app.route('/databasereader')
def databasereader():
    if not('user' in session):
        return redirect('/login')
    return DataBaseReaderModel.index(request.args)


'''
Медиа плеер
'''
@app.route('/audio')
def audio():
    if not('user' in session):
        return redirect('/login')
    return MediaPlayerModel.audio(request.args)


'''
Пользователи
'''
@app.route('/users')
def users():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return UsersModel.Users(user=user)

'''
Пользователи
'''
@app.route('/usercreate')
def usercreate():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return UsersModel.UserCreate(user=user)


'''
Логи
'''
@app.route('/logs')
def logs():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return StatisticModel.Logs(user=user)


'''
Контейнеры
'''
@app.route('/containers')
def containers():
    if not('user' in session):
        return redirect('/login')
    user = UsersModel.GetUser(id=session['user']['id'])
    return ContainersModel.index(user=user)

#=================== API ===================#



'''
Получение списка процессов
'''
@app.route('/api/getallprocess')
def getallprocess():
    return api.getAllProcess()

'''
Получение консоли
'''
@app.route('/api/getconsole')
def getconsole():
    return ConsoleModel.getConsole(request)

'''
Остановка консоли
'''
@app.route('/api/stopscript')
def stopscript():
    fullName = request.args.get('fullName')
    filePathHash = Functions.getNameHash(fullName)
    return ConsoleModel.stopscript(filePathHash)



'''
Управление файлами
'''
@app.route('/api/uploadfile', methods = ['GET', 'POST', 'DELETE'])
def uploadFile():
    user = UsersModel.GetUser(id=session['user']['id'])
    if user['role'] in ('admin', 'developer',):
        return api.uploadFile(request)
    else:
        redirect('/')

'''
Разархивирование
'''
@app.route('/api/uparchiv')
def uparchiv():
    user = UsersModel.GetUser(id=session['user']['id'])
    if user['role'] in ('admin', 'developer',):
        return api.uparchiv(request)
    else:
        redirect('/')

'''
Переиминовывание файла/папки
'''
@app.route('/api/renamefile')
def renameFile():
    user = UsersModel.GetUser(id=session['user']['id'])
    if user['role'] in ('admin', 'developer',):
        return api.renameFile(request.args)
    else:
        redirect('/')

'''
Удаление файла/папки
'''
@app.route('/api/deletefile')
def deleteFile():
    user = UsersModel.GetUser(id=session['user']['id'])
    if user['role'] in ('admin', 'developer',):
        return api.deleteFile(request.args)
    else:
        redirect('/')

'''
Создание новой папки
'''
@app.route('/api/createfolder')
def createFolder():
    user = UsersModel.GetUser(id=session['user']['id'])
    if user['role'] in ('admin', 'developer',):
        return api.createFolder(request.args)
    else:
        redirect('/')

'''
Создание нового файла
'''
@app.route('/api/createfile')
def createFile():
    user = UsersModel.GetUser(id=session['user']['id'])
    if user['role'] in ('admin', 'developer',):
        return api.createFile(request.args)
    else:
        redirect('/')

'''
Сохранение изменений в файле
'''
@app.route('/api/filesave', methods = ['GET', 'POST', 'DELETE'])
def fileSave():
    user = UsersModel.GetUser(id=session['user']['id'])
    if user['role'] in ('admin', 'developer',):
        return api.fileSave(request)
    else:
        redirect('/')

#===========================================#



#================== Error pages ==================#

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('/pages/errors/404.html'), 404

@app.errorhandler(500)
def page_server_error(e):
    # note that we set the 404 status explicitly
    return render_template('/pages/errors/500.html'), 500

#=================================================#

def StartServer():
    print('Inicializ DB')
    sqlighter.init_db(force=True)
    app.run(debug=False, host='0.0.0.0')