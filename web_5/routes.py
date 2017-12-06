from utils import log
from models import Message
from models import User

import random

# 这个函数用来保存所有的 messages
message_list = []
# session 可以在服务器端实现过期功能
session = {}


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了，管他呢，去他妈的文档
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    # 拼接html文件路径，比如 'templates/index.html'
    path = 'templates/' + name
    # 打开 'templates/index.html' 文件
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    """
    :param request: request实例
    :return: username 或者【游客】
    """
    # 从request中的cookies属性中拿user，比如 {'user': '3ssddljsfdajalde',} ，就可以拿到 '3ssddljsfdajalde'
    session_id = request.cookies.get('user', '')
    # 从session字典中拿session_id，就是 '3ssddljsfdajalde' 数据，如果拿得到说明这是登陆的user，否则就标记为【游客】
    username = session.get(session_id, '【游客】')
    # username = request.cookies.get('user', '【游客】')
    return username


# 根路径 / 的路由函数，比如 http://localhost:3000/ 一定会用到这个函数
def route_index(request):
    """
    :param request: request实例
    :return: HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n\r\n<html> ..... </html>
    """
    # 设置一个请求头
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    # 使用 template 函数打开 index.html 这个首页html文件
    body = template('index.html')
    # 拿到用户名，可能是username也可能是【游客】
    username = current_user(request)
    # 替换打开的index.html中的 {{username}} 为拿到用户名（username 或者【游客】）
    body = body.replace('{{username}}', username)
    # 拼接请求头和body HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n\r\n<html> ..... </html>
    r = header + '\r\n' + body
    # log('r是什么 -> ', r)
    return r.encode(encoding='utf-8')


def response_with_headers(headers, code=200):
    """
    headers = {
        'Content-Type': 'text/html',
        'Set-Cookie': 'user=asd23day3vgf33456',
    }
    """
    # headers -> 'HTTP/1.1 code VERY OK\r\n'
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    """
    header -> 
        HTTP/1.1 200 VERY OK\r\n
        Content-Type: text/html\r\n
        Set-Cookie: user=asd23day3vgf33456\r\n
    """
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


# 测试response_with_headers函数
# headers = {
#         'Content-Type': 'text/html',
#         'Set-Cookie': 'user=asd23day3vgf33456',
#     }
# log(response_with_headers(headers, code=200))


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    # 这里url是你想要重定向的地址，比如根目录 '/'
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    # 使用 response_with_headers 函数拿到响应，比如现在重定向到 '/'，那么得到的是，
    """
    HTTP/1.1 302 VERY OK\r\n
    Location: /\r\n\r\n
    """
    r = response_with_headers(headers, 302) + '\r\n'
    # log('重定向r是什么 -> ', r)
    return r.encode('utf-8')


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
        # User调用类方法new，因为User类继承自Model类，new是Model的类方法，所以User也拥有new方法，
        # @classmethod
        # def new(cls, form):
        #   m = cls(form)
        #   return m
        # 调用结果就是u是一个User类，并传递了form属性（form -> {'username': 'gua', 'password': '123'}）
        # u --> < User id: (None) username: (gua1) password: (123) >
        u = User.new(form)
        log('u = User.new(form)是什么 -> ', u)
        # u调用validate_login方法判断用户登录是否合法
        if u.validate_login():
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            # 把这个随机字符串当作u.username的令牌使用，比如{'asd23day3vgf33456': 'gua1'}，
            # 这样的话，必须知道令牌才能盗取用户名，那么这个难度就非常大了，这个作用主要是降低盗号风险
            session[session_id] = u.username
            # 为headers添加 'Set-Cookie' 字段，比如 {'Set-Cookie': 'user=asd23day3vgf33456'}
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # 下面是把用户名存入 cookie 中
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            result = '登录成功'
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
    log('login 的响应', r)
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册页面的路由函数
    """
    # 设置请求头
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
        u = User.new(form)
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


def route_message(request):
    """
    消息页面的路由函数
    """
    # 拿到用户名，可能是username也可能是【游客】
    username = current_user(request)
    # 如果是未登录的用户, 重定向到 '/'，因为我们不想让用户为登录情况下访问消息页面
    if username == '【游客】':
        log("**debug, route msg 未登录")
        # 利用重定向 redirect 函数让【游客】回到首页
        return redirect('/')
    log('本次请求的 method', request.method)
    # 如果用户不是【游客】，那么用户就可以在messages页面post数据
    if request.method == 'POST':
        # 把用户请求用form函数处理，比如 message=ccc&author=22 -> {'message': 'ccc', 'author': '22'}
        form = request.form()
        # 实例化msg, 比如< Message author: (22) message: (ccc) >
        msg = Message.new(form)
        # ('msg是什么 -> ', msg)
        log('post', form)
        # 把msg保存到 message_list 中
        message_list.append(msg)
        # 应该在这里保存 message_list
    # 设置请求头header
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    # 通过 template 读 html_basic.html 页面
    body = template('html_basic.html')
    # 把post的数据显示到页面{{messages}}标记的位置上
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    # 拼接请求
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 静态文件/static的路由函数，比如图片就需要用到这个函数
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
    '/messages': route_message,
}
