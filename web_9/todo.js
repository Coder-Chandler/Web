/*
1, 给 add button 绑定事件
2, 在事件处理函数中, 获取 input 的值
3, 用获取的值 组装一个 todo-cell HTML 字符串
4, 插入 todo-list 中
*/

var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

var todoTemplate = function(todo) {
    var t = `
        <div class="todo-cell">
            <button class="todo-delete">删除</button>
            <span>${todo}</span>
        </div>
    `
    return t
    /*
    上面的写法在 python 中是这样的
    t = """
    <div class="todo-cell">
        <button class="todo-delete">删除</button>
        <span>{}</span>
    </div>
    """.format(todo)
    */

}

var insertTodo = function(todo) {
    var todoCell = todoTemplate(todo)
    // 插入 todo-list
    var todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var b = e('#id-button-add')
// 注意, 第二个参数可以直接给出定义函数
b.addEventListener('click', function(){
    log('click')
    var input = e('#id-input-todo')
    var todo = input.value
    // log('todo ', todo)
    insertTodo(todo)
})

/*
给 删除 按钮绑定删除的事件
1, 绑定事件
2, 删除整个 todo-cell 元素
*/
var todoList = e('.todo-list')
// 事件响应函数会被传入一个参数, 就是事件本身
todoList.addEventListener('click', function(event){
    // log('click todolist', event)
    // 我们可以通过 event.target 来得到被点击的元素
    var self = event.target
    // log('被点击的元素是', self)
    // 通过比较被点击元素的 class 来判断元素是否是我们想要的
    // classList 属性保存了元素的所有 class
    // 在 HTML 中, 一个元素可以有多个 class, 用空格分开
    // log(self.classList)
    // 判断是否拥有某个 class 的方法如下
    if (self.classList.contains('todo-delete')) {
        log('点到了 删除按钮')
        // 删除 self 的父节点
        // parentElement 可以访问到元素的父节点
        self.parentElement.remove()
    } else {
        // log('点击的不是删除按钮******')
    }
})
