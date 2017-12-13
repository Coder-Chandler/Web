from routes.session import session
from utils import (
    log,
    redirect,
    template,
    http_response,
    current_user,
)


def main_index(request):
    username = current_user(request)
    if username == '游客':
        return redirect('/login')
    return redirect('/todo/index')


# 直接写函数名字不写 route 了
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    body = template('todo_index.html')
    return http_response(body)


route_dict = {
    '/': main_index,
    '/todo/index': index,
}
