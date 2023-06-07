import os



path_TOOL = os.path.abspath(os.getcwd())
path = f'{path_TOOL}/Tool/static/HTDOCS'
path_DataBase = f'{path_TOOL}/Tool/DATABASE'
path_cmd = f'{path_TOOL}/Tool/cmd'


icons = {
        '': 'file.png',
        'folder': 'folder.png',

        '7z': 'file-7z.png',
        'bmp': 'file-bmp.png',
        'css': 'file-css.png',
        'html': 'file-html.png',
        'jpg': 'file-jpg.png',
        'js': 'file-js.png',
        'png': 'file-png.png',
        'py': 'file-py.png',
        'rar': 'file-rar.png',
        'svg': 'file-svg.png',
        'tar': 'file-tar.png',
        'txt': 'file-txt.png',
        'zip': 'file-zip.png',
        'sqlite': 'file-database.png',
        'mp3': 'file-mp3.png',

        'md': 'file-markdown.png',
        'README.md': 'file-README.png',
    }


types_img = [
    'bmp',
    'png',
    'jpg',
    'svg',
    'gif',
]

types_arc = [
    'zip',
]