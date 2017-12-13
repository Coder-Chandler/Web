from utils import (
    log,
    redirect,
    json_response,
    template,
    current_user,
)
from models.todo import Todo
from models.todo import Comment
from models.user import User


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
def all(request):
    """
    返回所有 todo
    """
    todo_list = Todo.all()
    # 要转换为 dict 格式才行
    todos = [t.json() for t in todo_list]
    return json_response(todos)


def add(request):
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并返回给浏览器
    """
    # 得到浏览器发送的 json 格式数据
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json_loads()
    # 创建一个 todo
    t = Todo.new(form)
    # 把创建好的 todo 返回给浏览器
    return json_response(t.json())


def delete(request):
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    """
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.json())


def update(request):
    form = request.json_loads()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


def add_comment(request):
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并返回给浏览器
    """
    # 得到浏览器发送的 json 格式数据
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json_loads()
    # 创建一个 todo
    t = Comment.new(form)
    # 把创建好的 todo 返回给浏览器
    return json_response(t.json())


def login_required(route_function):
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f


route_dict = {
    '/api/todo/all': all,
    '/api/todo/add': login_required(add),
    '/api/todo/delete': delete,
    '/api/todo/update': update,

}
