
import flask
from Tool import CONSTANTS



def index(user=None):
    return flask.render_template(
        '/pages/statistic.html',
        user=user,
        page='statistic',
    )


def Logs(user=None):
    return flask.render_template(
        '/pages/logs.html',
        user=user,
        page='logs',
    )