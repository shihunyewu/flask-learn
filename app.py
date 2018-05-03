from flask import Flask, render_template, redirect, url_for, session, flash
from flask.ext.bootstrap import Bootstrap
import logging
from werkzeug.contrib.fixers import LighttpdCGIRootFix
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, validators
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
import os

# app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)

app = Flask(__name__)
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))
# 将数据库的 url 配置到 Flask 的 SQLALCHEMY_DATABASE_URI 键中
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 每次请求结束后都会自动提交数据库的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class Role(db.Model):
    """
    定义roles表
    同时定义 id，name 这两个字段
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 创建关联关系
    # relationship 的第一个的参数表明这个关系的另一端是哪个是模型
    # 如果模型尚未定义，可以使用字符串来指定
    # backref参数，向 User模型中添加一个 role属性，从而定义反向关系
    # 可以替代 role_id 访问 Role 模型，这样，获取的就是模型对象，而不是外键的值
    # 添加了 lazy = 'dynamic' 之后，每次使用user_role.users 会返回一个未执行的查询
    # 这样可以在其上添加过滤器
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        """
        返回一个具有可读性的字符串表示模型，可在调试和测试时使用
        :return:
        """
        return '<Role %r>' % self.name


class User(db.Model):
    """
    定义 users 表
    同时定义 id，username 这两个字段
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 定义外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        """
        返回一个具有可读性的字符串
        :return:
        """
        return '<User %r>' % self.username


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
        old_name = session.get('name')
        # 查询
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # return redirect(url_for('submit'))
    return render_template('submit.html',
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


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
    # db.drop_all() # 删除数据库
    # db.create_all()  # 第一次运行代码时，用来创建数据库
    # 后面的都是自己自行练习的 SQL 语句
    # admin_role = Role(name='Admin')
    # mod_role = Role(name='Moderator')
    # user_role = Role(name='User')
    # user_join = User(username='john', role=admin_role)
    # user_susan = User(username='susan', role=user_role)
    # user_david = User(username='david', role=user_role)
    #
    # # 通过会话管理对数据库所做的改动
    #
    # # db.session.add(admin_role)
    # # db.session.add(mod_role)
    # # db.session.add(user_role)
    # # db.session.add(user_join)
    # # db.session.add(user_susan)
    # # db.session.add(user_david)
    #
    # # 或者简写成
    # db.session.add_all([admin_role, mod_role, user_role,
    #                     user_join, user_susan, user_david])
    # # 使用 commit() 方法提交会话
    # db.session.commit()
    #
    # # 查看 admin_role.id，发现已经赋值了
    # print(admin_role.id)
    #
    # # 还有回滚操作，添加到数据库会话中的所有对象都会还原到他们在数据库时的状态
    # # db.session.rollback()
    #
    # # 修改行
    # admin_role.name = 'Administrator'
    # db.session.add(admin_role)
    # db.session.commit()
    #
    # # 删除行
    # db.session.delete(mod_role)
    # db.session.commit()
    #
    # # 注意插入与更新一样，提交数据库会话后才会执行
    #
    # # 查询
    # print(Role.query.all())
    # print(User.query.all())
    #
    # # 可以用过滤器来配置 query 对象进行更精确的数据库查询
    #
    # print(User.query.filter_by(role=user_role).all())
    # print('查看SQLAlchemy为查询生成的原生SQL查询语句：')
    # # 如果调用了 all() 就说明是执行了查询，没有 all() 或者其他方法，就没有执行查询
    # print(str(User.query.filter_by(role=user_role)))
    #
    # # 从关系的两端查询角色和用户之间的一对多关系
    # # 如果只写成 user_role.users 时，会隐含自动执行查询
    # # 隐含调用all() 返回一个用户列表，query对象时隐藏的，无法指定更精确的查询过滤器
    # # 因为它已经隐式地查询结束，只返回了结果
    # # 所以在定义关系的地方，加入 lazy = 'dynamic' 参数
    # users = user_role.users.order_by(User.username).all()
    # print(users)

    app.debug = True
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.run()
