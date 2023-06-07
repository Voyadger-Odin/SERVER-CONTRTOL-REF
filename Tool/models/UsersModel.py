import flask
from flask import session, redirect, render_template

from Tool import CONSTANTS
from Tool.Mechanics import Functions
from Tool.DATABASE import sqlighter


def GetUser(id):
    user = sqlighter.get_user(id=id)
    return {
        'id': user[0],
        'login': user[1],
        'role': user[2],
    }

def Login(request=None):
    user = sqlighter.login_user(login=request.form.get('login'), password=request.form.get('password'))
    if user is None:
        return redirect('/login')
    else:
        user_dict = {
            'id': user[0],
        }
        session['user'] = user_dict
        return redirect('/')

def Logout():
    session.pop('user')
    return redirect('/login')




def Users(user=None):
    users = sqlighter.get_all_users()
    return render_template(
        'pages/users/users.html',
        user=user,
        page='users',
        users=users
    )

def UserCreate(user=None):
    return render_template(
        'pages/users/usercreate.html',
        user=user,
        page='usercreate',
    )