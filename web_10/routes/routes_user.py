import random

from models.user import User
from routes.session import session
from utils import log
from utils import template


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def response_with_headers(headers, status_code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    # 拼接响应头和headers
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(location, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
        }
    headers['Location'] = location
    # 302 状态码的含义, Location 的作用
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def route_login(request):
    """
    登录页面的路由函数
    """
    # 设置headers
    headers = {
        'Content-Type': 'text/html',
    }
    log('login, cookies', request.cookies)

    if request.method == 'POST':
        # 调用 Request 类的 form 方法来处理 request 的 body 得到字典格式的body，
        # {'messages': 'goo', 'id': '22'}
        form = request.form()
        # 把 body 传给新实例化的u，这里的body其实就是用户登录输入的名字和密码
        u = User(form)
        # 验证u的登录是否合法
        if u.validate_login():
            # 在数据文件中找到登录用户的用户名
            user = User.find_by(username=u.username)
            # 设置 session（每次登录都会设置新的session给user.id）
            session_id = random_str()
            session[session_id] = user.id
            # 把代表用户名的session_id传给headers
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            log('headers response', headers)
            # 登录后定向到 /
            return redirect('/todo/index', headers)
    # 显示登录页面
    # template函数接受一个路径和一系列参数，读取模板并渲染返回
    body = template('login.html')
    # 通过response_with_headers函数拼接响应头和headers
    header = response_with_headers(headers)
    # 拼接 header 和 body 形成一个完整的HTTP响应
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    注册页面的路由函数
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # 调用 Request 类的 form 方法来处理 request 的 body 得到字典格式的body，
        # {'messages': 'goo', 'id': '22'}
        form = request.form()
        # 把 body 传给新实例化的u，这里的body其实就是用户注册输入的名字和密码
        u = User(form)
        # 验证u的注册是否合法
        if u.validate_register() is not None:
            # result = '注册成功<br> <pre>{}</pre>'.format(User.all())
            print('注册成功', u)
            # 注册成功后 定向到登录页面
            return redirect('/login')
        else:
            # 注册失败 定向到注册页面
            return redirect('/register')
    # 显示注册页面
    body = template('register.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


# 路由字典
route_dict = {
    '/login': route_login,
    '/register': route_register,
}
