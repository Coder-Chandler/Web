from utils import log
# from models import Message
from models import User

import random


# 这个函数用来保存所有的 messages
message_list = []
session = {}


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 210 VERY OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v)
                            for k, v in headers.items()])
    return header


def route_login(request):
    """
    :param request: request 实例
    :return:
        HTTP/1.1 200 VERY OK\r\n
        Content-Type: text/html\r\n
        Set-Cookie: user=asd23day3vgf33456\r\n\r\n
        <html>
            ..........
        </html>
    """
    # 设置请求头
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    }
    # log('login, headers', request.headers)
    log('login, cookies', request.cookies)
    # 拿到用户名，可能是username也可能是【游客】
    username = current_user(request)
    # 判断request的method，如果method是 'POST'，说明用户正在登录
    if request.method == 'POST':
        # 调用request的form方法，得到request中post的数据，
        # 比如'username=gua&password=123' -> {'username': 'gua', 'password': '123'}
        form = request.form()
        # 实例化u，结果就是u是一个User类，并传递了form属性（form -> {'username': 'gua', 'password': '123'}）
        # u --> < User id: (None) username: (gua1) password: (123) >
        u = User(form)
        # u调用validate_login方法判断用户登录是否合法
        if u.validate_login():
            # session_id = random_str()
            # session[session_id] = u.username
            # headers['Set-Cookie'] = 'user={}'.format(session_id)
            # 找到这个user的数据，比如< User password: (1212) username: (gua1) id: (1) >
            user = User.find_by(username=u.username)
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            # 把这个随机字符串当作user.id的令牌使用，比如{'wqewqdefew3223432': '1'}，
            # 这样的话，必须知道令牌才能盗取用户名，那么这个难度就非常大了，这个作用主要是降低盗号风险
            session[session_id] = user.id
            # 为headers添加 'Set-Cookie' 字段，比如 {'Set-Cookie': 'user=asd23day3vgf33456'}
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # headers['Set-Cookie'] = 'user_id={}'.format(user.id)
            result = '登录成功'
            log('headers response', headers)
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    # 用 template 函数打开 login.html 文件
    body = template('login.html')
    # 把login.html页面的{{result}}标记位置替换为result
    body = body.replace('{{result}}', result)
    # 把login.html页面的{{username}}标记位置替换为username
    body = body.replace('{{username}}', username)
    # 通过response_with_headers函数得到请求头，比如
    """
    headers = {
        'Content-Type': 'text/html',
        'Set-Cookie': 'user=asd23day3vgf33456',
    }
    """
    # 通过response_with_headers函数拿到服务器响应数据，比如，
    """
    header -> 
        HTTP/1.1 200 VERY OK\r\n
        Content-Type: text/html\r\n
        Set-Cookie: user=asd23day3vgf33456\r\n
    """
    header = response_with_headers(headers)
    # 把响应和body拼接起来，比如，
    """
        HTTP/1.1 200 VERY OK\r\n
        Content-Type: text/html\r\n
        Set-Cookie: user=asd23day3vgf33456\r\n\r\n
        <html>
            ..........
        </html>
    """
    r = header + '\r\n' + body
    # log('login', r)
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册页面的路由函数
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # 调用request的form方法，得到request中post的数据，
        # 比如'username=gua&password=123' -> {'username': 'gua', 'password': '123'}
        form = request.form()
        # User调用类方法new，因为User类继承自Model类，new是Model的类方法，所以User也拥有new方法，
        # @classmethod
        # def new(cls, form):
        #   m = cls(form)
        #   return m
        # 调用结果就是u是一个User类，并传递了form属性（form -> {'username': 'gua', 'password': '123'}）
        u = User(form)
        # u调用validate_register方法判断用户的注册是否符合要求
        if u.validate_register():
            # 注册符合要求就保存至数据文件中
            u.save()
            # 在页面显示注册成功以及所有的用户数据
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    # 用template函数显示 register.html 页面
    body = template('register.html')
    # 在 register.html 页面 {{result}} 标记位置显示 result
    body = body.replace('{{result}}', result)
    # 补全请求
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# def route_message(request):
#     """
#     消息页面的路由函数
#     """
#     log('本次请求的 method', request.method)
#     if request.method == 'POST':
#         form = request.form()
#         msg = Message(form)
#         log('post', form)
#         message_list.append(msg)
#         # 应该在这里保存 message_list
#     header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
#     # body = '<h1>消息版</h1>'
#     body = template('html_basic.html')
#     msgs = '<br>'.join([str(m) for m in message_list])
#     body = body.replace('{{messages}}', msgs)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


def route_profile(request):
    log('profile cookies', request.cookies)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = template('profile.html')
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    user = ''
    if user_id != -1:
        user = User.find_by(id=int(user_id))
    body = body.replace('{{user}}', str(user))
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    :param request: request实例
    :return: b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\nGIF89aI...................
    """
    # 从request实例的query属性中拿到 file 这个字段，如果query是 {'file': 'doge1.gif'}，那么filename等于'doge1.gif'，
    # 如果没有file就赋值为 'doge.gif'
    filename = request.query.get('file', 'doge.gif')
    # 把 'static/' 和 filename 拼接 -> 'static/doge1.gif'
    path = 'static/' + filename
    # 取文件中找 'static/doge1.gif' 这个图片，并以rb（二进制）的方式打开
    with open(path, 'rb') as f:
        # 设置一个请求头header
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        # 把请求头和读取出来的图片拼接
        # b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\nGIF89aI\x00A\x00\x....................
        img = header + f.read()
        # log('image是什么 -> ', img)
        return img


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    # '/messages': route_message,
    '/profile':route_profile,
}
