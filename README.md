	return response
```

可以重定向到其他链接
```python
from flask import redirect
@app.route('/')
def index():
	return redirect('http://www.example.com')
```

还有一种特殊的响应由 abort 函数生成。

```python
from flask import abort
@app.route('/user/<id>')
def get_user(id):
	user = load_user(id)
	if not user:
	abort(404)
	return '<h1>Hello, %s</h1>' % user.name
```
abort 不会讲控制权还给调用它的函数，而是抛出异常，将控制权交给服务器

##### 2.6 Flask扩展

### 第 3 章 模板

##### 3.1 Jinja2 模板引擎

* 3.1.1 渲染模板

* 3.1.2 变量
模板中使用 {{name}} 结构表示一个变量，jinja2 能够识别所有类型的变量，像列表、字典和对象。

	* 可以使用过滤器修改变量，比如
	```html
	<!-- 这里的 captitalize 是将值的首字母转换成大写，其他字母转换成小写字母 -->
	Hello,{{name | capitalize}}
	```
	还有很多的可选操作
* 3.1.3 控制结构

	* 条件控制语句
	```html
	{% if user %}
		<li>{{comment}} </li>
	{% else %}
		Hello,Stranger!
	{% endif %}
	```

	* 循环语句
	```html
	{% for	comment in comments %}
		<li>{{comment}} </li>
	{% endfor %}
	```

	* 支持宏
	宏类似于函数
	```html
	{% #这里的 macro 是定义宏的关键字？%}
	{% macro render_comment(comment) %}
		<li>{{ comment }}</li>
	{% endmacro %}
	```

	* 类似于模块调用

	```python
	{% #macros.html%}
	{% macro render_comment(comment) %}
		<li>{{ comment }}</li>
	{% endmacro %}
	```

	```html
	{% #index.html%}
	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Hello</title>
	</head>
	<body>
    {%# 改用引用别的模块中的函数%}
	{% import 'macros.html' as macros %}
	<ul>
		{% for comment in comments %}
        	{%# 像引入包一样引入模块，但是调用时要用现在的包名%}
			{{ macros.render_comment(comment) }}
		{% endfor %}
	</ul>

	</body>
	</html>
	```

	* 拼接 html

	```html
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Hello</title>
	</head>
	<body>
    {%#  top.html 作为网站的头部 %}
	{% include 'top.html' %}
	{{ word|capitalize }}
	{% if user %}
		Hello,{{ user }}
	{% else %}
		Hello,Stranger!
	{% endif %}
	</body>
	</html>

	```

	* 模板继承

		在子模板的开头定义了”{% extend ‘parent.html’ %}”语句来声明继承，此后在子模板中由”{% block block_name %}”和”{% endblock %}”所包括的语句块，将会替换父模板中同样由”{% block block_name %}”和”{% endblock %}”所包括的部分。

		这就是块的功能，模板语句的替换。这里要注意几个点：

		1. 模板不支持多继承，也就是子模板中定义的块，不可能同时被两个父模板替换。
		2. 模板中不能定义多个同名的块，子模板和父模板都不行，因为这样无法知道要替换哪一个部分的内容。

		另外，我们建议在”endblock”关键字后也加上块名，比如”{% endblock block_name %}”。虽然对程序没什么作用，但是当有多个块嵌套时，可读性好很多。

		如果父模板中的块里有内容不想被子模板替换怎么办？在 block 结构中使用 super()

		[jinja2模板的继承](http://www.bjhee.com/jinja2-block-macro.html)

* 3.3 使用 Flask-Bootstrap 继承 Twitter Bootstrap
	[Bootstrap](http://getbootstrap.com/)

	很强，从 Flask-Bootstrap 上继承了很多已经定义好了的 Block 块。


* 3.4 链接
url_for() 函数最简单的是以视图函数名作为参数，返回对应的URL。
```python
url_for('index', page=2) 的返回结果是/index？page=2
```

* 3.5 静态文件
```python
url_for('static', filename='css/styles.css', _external=True) # 参数名一定要是 filename
```

* 3.6 使用Flask-momen本地化日期和时间

##### 第 4 章 Web 表单

* 4.2 表单类 wtf
	Flask-WTF 可以处理 Web 表单。

* 4.3 将表单渲染成 HTML

* 4.4 在视图函数中处理表单

* 4.5 重定向和用户会话

* 4.6 Flash 消息
	* Flash 用来响应用户的请求，给用户返回一个消息
	主要就是 flash() 和 get_flashed_messages()的应用。在app.py中使用 flash()放警告信息，在page中用 get_flashed_messages() 取信息。

##### 第 5 章 数据库

* 5.5 使用 Flask-SQLAlchemy 管理数据库

| 数据库引擎 | URL |
|--------|--------|
|   MySQL     |    mysql://username:password@hostname/database    |
| SQLite（Windows） |sqlite:///c:/absolute/path/to/database |

hostname代表主机，database 代表数据库名。SQLite是文件数据库，不需要服务器，所以database是硬盘上文件的文件名。

**程序中使用数据URL必须保存到 Flask 配置对象的SQLALCHEMY_DATABASE_URI键中**。

* 5.11.2 创建迁移脚本
脚本中有两个函数，分别是upgrade() 和 downgrade().
	* upgrade()函数把迁移中的改动应用到数据库中
	对第一个迁移来说， 其作用和调用db.create_all() 方法一样。但在后续的迁移中，upgrade 命令能把改动应用到数据库中，且不影响其中保存的数据。
	* downgrade() 函数将改动删除。
	因此数据库可重设到修改历史的任意一点。


##### 第 6 章 电子邮件

##### 第 7 章 大型程序的结构

* 官方推荐的目录结构

```python
|-flasky
	|-app/
		|-templates/
		|-static/
		|-main/
            |-__init__.py
            |-errors.py
            |-forms.py
            |-views.py
        |-__init__.py
        |-email.py
        |-models.py
|-migrations/
|-tests/
	|-__init__.py
    |-test*.py
|-venv/
|-requirements.txt
|-config.py
|-manage.py
```

* 含义
	* requirement.txt 列出所有依赖的包

* 配置选项

##### 第 8 章 用户认证

* Flask的认证扩展
	* Flask-Login：管理已经登录用户的会话
	* Werkzeug：计算密码散列值并进行核对
	* itsdangerous：生成并核对加密安全令牌

* 密码安全性：
	数据库直接存储用户的密码是很危险的
    应该存储密码的散列值
    密码作为输入，使用密码加密算法转换面，最终得到加密字符串。
    计算散列值要求是可以浮现的。
* Werkzeug实现密码散列

* 存在问题：
	前面的数据迁移和邮件没有看，另外创建orm不熟，创建表单不熟吗，创建模板不熟。

* 8.3



















##### 参考文档

《FlaskWeb开发》