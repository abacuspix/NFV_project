# coding:utf-8
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index_view(arg=None):
    import pdb;
    pdb.set_trace()  # @TODO remove me before commit
    return 'Arg is %s' % arg


if __name__ == '__main__':
    app.debug = True
    app.run()
