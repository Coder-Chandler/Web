from models.message import Message
from models.user import User
from utils import log


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            log('注册成功后的model -> ', User.all())
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# message_list 存储了所有的 message
message_list = []


def route_message(request):
    log('本次请求的 method -> ', (request.method,))
    if request.method == 'POST':
        # message=hello&author=gua --> {'message':'hello', 'author': 'gua'}
        form = request.form()

        # {'message': 'hello', 'author': 'gua'} --> < Message author: (gua) message: (hello) >
        msg = Message.new(form)

        log('post表单 -> ', form, type(form))
        log('messages -> ', msg, type(msg))

        # [< Message author: (gua) message: (hello) >]
        message_list.append(msg)
        log('message_list -> ', message_list)
        # 应该在这里保存 message_list

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    # '#'.join(['a', 'b', 'c']) 的结果是 'a#b#c'
    # [< Message author: (gua) message: (hello) >] -> '< Message author: (gua) message: (hello) >'
    msgs = '<br>'.join([str(m) for m in message_list])
    log('messages -> ', msgs, type(msgs))
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


"""
method POST
2017/12/03 23:43:40 post {'message': 'hello', 'author': 'gua'} <class 'dict'>
2017/12/03 23:43:40 msg < Message
author: (gua)
message: (hello) >
 <class 'models.message.Message'>
2017/12/03 23:43:40 message_list [< Message
author: (gua)
message: (hello) >
]
2017/12/03 23:43:40 msgs < Message
author: (gua)
message: (hello) >


method GET
2017/12/03 23:45:25 msgs < Message
author: (gua)
message: (hello) >

"""


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    <img src="/static?file=doge.gif"/>
    GET /static?file=doge.gif
    path, query = response_for_path('/static?file=doge.gif')
    path  '/static'
    query = {
        'file', 'doge.gif',
    }
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}
