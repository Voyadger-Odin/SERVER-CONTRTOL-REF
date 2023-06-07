


import flask
from mutagen.easyid3 import EasyID3



def audio(args):
    pathFile = args.get('audio')

    audio = EasyID3(f'Tool/static/HTDOCS{pathFile}')

    title = pathFile.split('/')[-1].split('.')[0]
    artist = ''

    if not(audio is None) and (audio != {}):
        if ('title' in audio):
            title = audio['title'][0]
        if ('artist' in audio):
            artist = audio['artist'][0]
        if ('album' in audio):
            album = audio['album'][0]
            if ('date' in audio):
                album += f' - {audio["date"][0]}'
            title += f' ({album})'

    return flask.render_template(
        '/pages/media/audio.html',
        audio = f'HTDOCS{pathFile}',
        title=title,
        artist = artist
    )

