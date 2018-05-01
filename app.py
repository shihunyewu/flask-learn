from flask import Flask, render_template, redirect, url_for,session
from flask.ext.bootstrap import Bootstrap
import logging
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,validators
from wtforms.validators import Required

# app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)

app = Flask(__name__)
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'


class NameForm(Form):
    """
    这个表单中的字段都定义为类变量
    其中表单中有一个名为 name 的文本字段，
    validators 指定一个由验证函数组成的列表，在接收用户提交的数据之前验证数据，验证函数Required()确保提交的字符不为空
    一个名为 submit 的提交按钮
    这里很神奇
    """
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/submit')
def submit():
    myform = NameForm()
    return render_template('submit.html', form=myform)


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('submit'))
    return render_template('submit.html', form=form, name=session.get('name'))


@app.route('/')
def root():
    word = 'hello world'
    user = 'sgy'
    comments = ['I quit', 'bye', 'following', 'keep following']
    return render_template('index.html', word=word, user=user, comments=comments, name='sgy')


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name='sgy'):
    return render_template('hello.html', name=name)


@app.route('/fake')
def fake():
    return redirect(url_for('hello', name='john'))  # 重新定向网页


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.debug = False
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run()
