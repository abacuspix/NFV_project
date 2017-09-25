# coding:utf-8
from flask import Flask
from flask_admin import Admin, BaseView, expose


class ReportsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('reports.html')


app = Flask(__name__)
admin = Admin(app)
admin.add_view(ReportsView(name='Reports Page'))

if __name__ == '__main__':
    app.debug = True
    app.run()