
import flask
from Tool import CONSTANTS



def index(user=None):
    return flask.render_template(
        '/pages/containers/containers.html',
        user=user,
        page='containers',
    )
