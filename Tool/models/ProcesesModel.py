
import flask
from Tool import CONSTANTS



def index(user=None):
    return flask.render_template(
        '/pages/proceses.html',
        user=user,
        page='proceses',
    )