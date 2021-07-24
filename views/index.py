import flask
from flask import json,  request
from flask.views import View


class IndexView(View):
    def dispatch_request(self):
        return flask.render_template('index.html', )


