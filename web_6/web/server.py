import socket
import urllib.parse

from utils import log

from routes_static import route_static

from routes_simpletodo import route_dict as simpletodo_routes
from routes_user import route_dict as user_routes


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        """
        {
            'Host': 'localhost:3000',
            'Connection': 'keep-alive',
            'Content-Length': '25',

            ..............

            'Cookie': 'user=3ssddljsfdajalde',
        }
        :return:
            {
                'user': '3ssddljsfdajalde',
            }
        """
        # 从headers里面拿到Cookie 'user=3ssddljsfdajalde' ,没有的话就设置cookie为空字符串
        cookies = self.headers.get('Cookie', '')
        # log("cookies = self.headers.get('Cookie', '')", cookies)
        # 把cookies数据按照 '; ' 分割，得到['user=ff9sca8daj2gidke']
        kvs = cookies.split('; ')
        log('add cookies', kvs)
        # 遍历['user=ff9sca8daj2gidke']
        for kv in kvs:
            # 判断 '=' 是否在 'user=ff9sca8daj2gidke' 中
            if '=' in kv:
                # 等号两边分别为key和value传入cookies这个dict中
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        """
        :param header:
            Host: localhost:3000
            Connection: keep-alive
            Content-Length: 25
            Cache-Control: max-age=0
            User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
            Upgrade-Insecure-Requests: 1
            Origin: http://localhost:3000
            Content-Type: application/x-www-form-urlencoded
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
            Referer: http://localhost:3000/login
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
            Cookie: user=3ssddljsfdajalde
        :return:
            {
                'Host': 'localhost:3000',
                'Connection': 'keep-alive',
                'Content-Length': '25',
                'Cache-Control': 'max-age=0',

                ..............

                'Cookie': 'user=3ssddljsfdajalde',
            }
        """
        # 清空self之前的headers
        self.headers = {}
        lines = header
        # 遍历headers每一行数据
        for line in lines:
            # 把每一行headers的数据按照 ': ' 分割
            k, v = line.split(': ', 1)
            # 把 ': ' 之前的作为key，之后的作为value传入headers
            self.headers[k] = v
        # 清除self之前的cookies
        self.cookies = {}
        self.add_cookies()

    def form(self):
        """
        :param: 'username=gua&password=123'
        :return: {'username': 'gua', 'password': '123'}
        """
        # log('self.body 是什么 -> ', self.body)
        # self.body是post请求的body，比如输入的用户名和密码字段 username=gua&password=123，
        # 利用unquote函数处理 self.body 例子：unquote('abc%20def') -> 'abc def'
        # unquote('username=gua&password=123') -> 'username=gua&password=123'
        body = urllib.parse.unquote(self.body)
        # 分割 'username=gua&password=123' 得到 ['username=gua', 'password=123']
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            # {'username': 'gua', 'password': '123'}
            f[k] = v
        return f


#
request = Request()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    :param path: '/todo/edit?id=1'
    :return: 'todo/edit', {'id': '1'}
    """
    # 在path中找 '?' ，因为如果存在 '?' 说明有变量名和赋值，比如?id=1意思是给变量id赋值，值为1。
    # 再比如这个地址 http://localhost:3000/messages?messages=22 '?'后面意思是给messages这个变量赋值，值为22
    # 作为 '/todo/edit?id=1' 这个path，index就不等于-1，因为find到了 '?'，如果没有'?'，就返回传进来的path和空字典
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        # 按照 '?' 分割 '/todo/edit?id=1' --> ['todo/edit', 'id=1'] -->  path='todo/edit', query_string='id=1'
        path, query_string = path.split('?', 1)
        # 把query_string也就是 'id=1' 按照 '&' 分割，显然这个 '/todo/edit?id=1' 例子没有，那么args就等于['id=1']
        args = query_string.split('&')
        query = {}
        # 遍历 ['id=1']
        for arg in args:
            # 按照 '=' 分割 ['id=1']
            k, v = arg.split('=')
            # 把等号两边数据传入query这个dict
            query[k] = v
        return path, query


def response_for_path(path):
    """
    :param path: '/todo/edit?id=1'
    :return:
        HTTP/1.1 200 VERY OK\r\n
        Content-Type: text/html\r\n
        Set-Cookie: user=asd23day3vgf33456\r\n\r\n
        <html>
            ..........
        </html>
    """
    # 首先利用 parsed_path 函数处理path得到 'todo/edit', {'id': '1'}
    path, query = parsed_path(path)
    # 把 'todo/edit' 传给request
    request.path = path
    # 把 {'id': '1'} 传给request
    request.query = query
    log('path and query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    # 把路由函数全部存入dict
    r = {
        '/static': route_static,
    }
    # 注册外部的路由
    r.update(simpletodo_routes)
    r.update(user_routes)
    # 按照path来确定用哪一个路由函数来处理，比如 'todo/edit' 就要用 todo_route 中的 edit 函数来处理，
    # 那么这里的response就等于edit这个函数
    response = r.get(path, error)
    # 上面的response如果等于edit这个函数，那么 response(request) 就相当于 edit(request)
    # log('现在request是什么 -> ', response(request))
    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            log('完整请求')
            log(r.replace('\r\n', '\n'))
            log('请求结束')
            # 以下是登陆的原始请求r
            """
            POST /login HTTP/1.1
            Host: localhost:3000
            Connection: keep-alive
            Content-Length: 25
            Cache-Control: max-age=0
            Origin: http://localhost:3000
            Upgrade-Insecure-Requests: 1
            Content-Type: application/x-www-form-urlencoded
            User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
            Referer: http://localhost:3000/login
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9,en;q=0.8

            username=gua&password=123
            """

            # log('ip and request, {}\n{}'.format(address, r))
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            # 获得请求的路径（比如 '/'  '/login' 等等)，这里用空格来split，
            # 所以得到的是原始请求第一行第一个空格后的请求path
            path = r.split()[1]
            # 设置 request 的 method，和上面得到path的方法一样，
            # 请求的第一行第一个就是方法（Get or Post）
            request.method = r.split()[0]
            # 设置request的headers，首先这里用 '\r\n\r\n' 2个回车符号来split请求，并且只split一次，
            # 那么就分割了最下面的body和上面的请求行以及请求头headers，再切片至第0个，就是除去body
            # 剩下的请求行以及请求头headers，再对请求行以及请求头headers以 '\r\n'片 回车符split并切片[1:]，
            # 得到的是请求头headers，再把请求头headers数据传入 add_headers 函数中
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            # 把 body 放入 request 中, 这里用'\r\n\r\n' 2个回车符号来split请求，并且只split一次，
            # 那么就分割了最下面的body和上面的请求行以及请求头headers，再切片至第1个，就拿到了body
            # ['username=gua&password=123']
            request.body = r.split('\r\n\r\n', 1)[1]
            # 用 response_for_path 函数来得到 path 对应的响应内容,比如，
            """
            HTTP/1.1 200 VERY OK\r\n
            Content-Type: text/html\r\n
            Set-Cookie: user=asd23day3vgf33456\r\n\r\n
            <html>
                ..........
            </html>
            """
            response = response_for_path(path)
            # 把响应发送给客户端然后显示给用户看
            connection.sendall(response)
            log('完整响应')
            try:
                log(response.decode('utf-8').replace('\r\n', '\n'))
            except Exception as e:
                log('异常', e)
            log('响应结束')
            # 处理完请求, 关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 上过基础课的请复习函数, 新同学自行搜索
    run(**config)
