# coding: utf-8

import socket

"""
课 2 上课用品
2017/02/16

本次上课的主要内容有
0, 请注意代码的格式和规范(PEP8)
1, 规范化生成响应
2, HTTP 头
3, 几个常用 HTML 标签及其用法
4, 浏览器向服务器传递参数的两种方式
"""


def log(*args, **kwargs):
    """
    用这个 log 替代 print
    """
    print('log', *args, **kwargs)


def route_index():
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello Gua</h1><img src="/doge.gif">'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def page(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


def route_msg():
    """
    msg 页面的处理函数
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('html_basic.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    """
    图片的处理函数, 读取图片并生成响应返回
    """
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


def error(code=404):
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


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/': route_index,
        '/doge.gif': route_image,
        '/msg': route_msg,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            log('raw, ', request)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                # 因为 chrome 会发送空请求导致 split 得到空 list
                # 所以这里用 try 防止程序崩溃
                path = request.split()[1]
                # log('path', path)
                # 用 response_for_path 函数来得到 path 对应的响应内容
                response = response_for_path(path)
                # 把响应发送给客户端
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            # 处理完请求, 关闭连接
            connection.close()


def main():
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 群里问或者看书/搜索 关键字参数
    run(**config)


if __name__ == '__main__':
    main()


"""
log raw,  b'POST / HTTP/1.1\r\nHost: localhost:3000\r\nConnection: keep-alive\r\nContent-Length: 11\r\nCache-Control: max-age=0\r\nOrigin: http://localhost:3000\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nReferer: http://localhost:3000/msg\r\nAccept-Encoding: gzip, deflate, br\r\nAccept-Language: en-US,en;q=0.8\r\nCookie: Pycharm-df207d35=600adc10-1f5d
-46ff-b99f-861b091847e7\r\n\r\nmessage=gua'

log ip and request, ('127.0.0.1', 51905)
POST / HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Content-Length: 11

message=gua


GET /?message=GUA HTTP/1.1
Host: localhost:3000
Connection: keep-alive



"""