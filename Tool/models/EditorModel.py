
from flask import render_template
from Tool import CONSTANTS


def editor(args, user=None):
    pathFile = args.get('path')
    nameFile = args.get('name')
    fileType = nameFile.split('.')[-1]

    fullPath = f'{CONSTANTS.path}{pathFile}/{nameFile}'

    f = open(fullPath, "r", encoding='utf-8')
    data = f.read()
    f.close()

    #return data
    return render_template(
        'pages/editor.html',
        user=user,
        data=data,
        type=fileType,
        nameFile=nameFile
    )
