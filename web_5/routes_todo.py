from utils import log
from todo import Todo
from models import User
from routes import current_user


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(headers, code=200):
    """
    :param headers: headers = {'Content-Type': 'text/html',}
    :param code: code
    :return:
        HTTP/1.1 200 VERY OK\r\n
        Content-Type: text/html\r\n
    """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    r = response_with_headers(headers, 302) + '\r\n'
    # log('2, 服务器解析出表单的数据, 并且增加一条新数据, 并返回 302 响应', r)
    return r.encode('utf-8')


def login_required(route_function):
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f


def index(request):
    """
    /todo 页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 如果已经登录，那么获取这个登录用户下面的所有数据
    todo_list = Todo.find_all(user_id=u.id)
    # 下面这行生成一个 html 字符串
    # todo_html = ''.join(['<h3>{} : {} </h3>'.format(t.id, t.title)
    #                      for t in todo_list])
    # 上面一行列表推倒的代码相当于下面几行
    todos = []
    # 遍历当前用户下的所有数据
    for t in todo_list:
        # 每一个数据后面都跟着一个编辑和删除的链接
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        # 把用户的每一条数据的id、标题title、编辑数据链接、删除数据链接放入todos这个list中
        # 比如,['<h3>3 : 喝水 <a href="/todo/edit?id=3">编辑</a> <a href="/todo/delete?id=3">删除</a></h3>',...]
        s = '<h3>{} : {} {} {}</h3>'.format(t.id, t.title, edit_link, delete_link)
        todos.append(s)
        # log('todos.append(s) 是什么 -> ', todos)
    # 把todos这个list做join操作，得到比如
    # '<h3>3 : 喝水 <a href="/todo/edit?id=3">编辑</a> <a href="/todo/delete?id=3">删除</a></h3><h3>....</h3> ...'
    todo_html = ''.join(todos)
    # log('todo_html -> ', todo_html)
    body = template('todo_index.html')
    # 替换todo_index.html模板文件中的{{todos}}标记字符串为todo_html
    body = body.replace('{{todos}}', todo_html)
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    # headers上面已经设置过了， headers = {'Content-Type': 'text/html',}
    # 返回请求头， HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n
    header = response_with_headers(headers)
    # 把请求头和body拼接
    """
    HTTP/1.1 200 VERY OK\r\n
    Content-Type: text/html\r\n\r\n
    <html>
        .........
    </html>
    
    """
    r = header + '\r\n' + body
    log('4.服务器给浏览器一个页面响应', r)
    return r.encode(encoding='utf-8')


def edit(request):
    """
    /todo/edit 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 todo 的 id，如果获取不到就设置为-1
    todo_id = int(request.query.get('id', -1))
    # 找到当前被编辑的条目的数据，按照当前编辑的 todo 的 id来寻找，
    # 比如编辑 {"id": 3, "title": "喝水", "user_id": 1}，那么按照"id": 3取数据文件中查询
    # 比如 t = < Todo id: (3) title: (喝水) user_id: (1) >
    t = Todo.find_by(id=todo_id)
    # log('找到当前登录用户要编辑的数据的对应id', t)
    # 判断被编辑的这个数据对应的用户id（t.user_id）和编辑这个数据的用户id（u.id）是否一致
    # 比如 t.user_id = 1， u.id = 1
    # 如果两者相等说明登录用户在修改自己的数据，不相等说明登录用户在修改别人的数据，那这个是不允许的，就重定向到登录页面
    if t.user_id != u.id:
        return redirect('/login')
    # if todo_id < 1:
    #     return error(404)
    # 如果 t.user_id 和 u.id 相等，先读todo_edit.html 页面
    # 再替换模板文件todo_edit.html中的标记字符串{{todo_id}}为当前被编辑的todo的数据的id，
    # {{todo_title}}为当前被编辑的todo的数据的title
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    # 通过response_with_headers拿到服务器响应，headers上面设置了，headers = {'Content-Type': 'text/html',}
    # 返回请求头， HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n
    header = response_with_headers(headers)
    # 把请求头和body拼接
    """
    HTTP/1.1 200 VERY OK\r\n
    Content-Type: text/html\r\n\r\n
    <html>
        .........
    </html>

    """
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    # 判断请求方法是否是POST
    if request.method == 'POST':
        # 'title=aaa'
        # {'title': 'aaa'}
        # 用form函数处理请求
        # form的用法
        """
        :param: 'username=gua&password=123'
        :return: {'username': 'gua', 'password': '123'}
        """
        form = request.form()
        # 实例化t，把请求的form传给t
        t = Todo.new(form)
        # 把登录用户的id传给这条新加的todo数据
        t.user_id = u.id
        # 再把这条数据保存至数据文件
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def update(request):
    """
    用于增加新 todo 的路由函数
    """
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 修改并且保存 todo
        # 用form函数处理请求
        # form的用法
        """
        :param: 'username=gua&password=123'
        :return: {'username': 'gua', 'password': '123'}
        """
        form = request.form()
        print('debug update', form)
        # 拿到修改的数据的id，有可能用户修改数据的时候也把id改了
        todo_id = int(form.get('id', -1))
        #
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def delete_todo(request):
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前删除的 todo 的 id
    todo_id = int(request.query.get('id', -1))
    # 找到当前被删除的条目的数据，按照当前编辑的 todo 的 id来寻找，
    # 比如编辑 {"id": 3, "title": "喝水", "user_id": 1}，那么按照"id": 3取数据文件中查询
    # 比如 t = < Todo id: (3) title: (喝水) user_id: (1) >
    t = Todo.find_by(id=todo_id)
    # log('找到当前登录用户要编辑的数据的对应id', t)
    # 判断被删除的这个数据对应的用户id（t.user_id）和编辑这个数据的用户id（u.id）是否一致
    # 比如 t.user_id = 1， u.id = 1
    # 如果两者相等说明登录用户在修改自己的数据，不相等说明登录用户在修改别人的数据，那这个是不允许的，就重定向到登录页面
    if t.user_id != u.id:
        return redirect('/login')
    # 如果t不是None，意思就是说被删除的这个数据是存在的，那么就用remove函数把t删除掉
    if t is not None:
        t.remove()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # GET 请求, 显示页面
    '/todo': index,
    '/todo/edit': edit,
    # POST 请求, 处理数据
    '/todo/add': login_required(add),
    '/todo/update': update,
    '/todo/delete': delete_todo,
}
