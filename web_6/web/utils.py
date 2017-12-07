from jinja2 import Environment, FileSystemLoader
import os.path
import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


# __file__ 就是本文件的名字
# 得到用于加载模板的目录
path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def template(path, **kwargs):
    """
    本函数接受一个路径和一系列参数
    读取模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)


def response_with_headers(headers, status_code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(location, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
        h.update(headers)
    h['Location'] = location
    # 302 状态码的含义, Location 的作用
    header = response_with_headers(h, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def http_response(body, headers=None):
    """
    headers 是可选的字典格式的 HTTP 头
    """
    # 设置请求头
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # 判断headers是否为None，如果不为None，拼接header和headers里面的数据
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    # 拼接header和body
    r = header + '\r\n' + body
    """
    HTTP/1.1 200 VERY OK\r\n
    Content-Type: text/html\r\n
    
    <html>
        ......
    </html>
    """
    return r.encode(encoding='utf-8')
