var timeString = function(timestamp) {
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

var commentsTemplate = function(comments) {
    var html = ''
    for(var i = 0; i < comments.length; i++) {
        var c = comments[i]
        var t = `
            <div>
                ${c.content}
            </div>
        `
        html += t
    }
    return html
}

var WeiboTemplate = function(weibo) {
    var content = weibo.content
    var id = weibo.id
    // log('weibo.ut', weibo.ut)
    var ut = timeString(weibo.ut)
    // log('ut', ut)
    var comments = commentsTemplate(weibo.comments)
    var t = `
        <div class='weibo-cell' id='weibo-${id}' data-id=${id}>
            <span class='weibo-content'>${content}</span>
            <time class='weibo-ut'>${ut}</time>
            <button class="weibo-edit">编辑微博</button>
            <button class="weibo-delete">删除微博</button>
            <div class="comment-list">
                ${comments}
            </div>
            <div class="comment-form">
                <input type="hidden" name="weibo_id" value="">
                <input name="content">
                <br>
                <button class="comment-add">添加评论</button>
            </div>
        </div>
    `
    return t
    /*
    上面的写法在 python 中是这样的
    t = """
    <div class="Weibo-cell">
        <button class="Weibo-delete">删除</button>
        <span>{}</span>
    </div>
    """.format(Weibo)
    */
}

var insertWeibo = function(weibo) {
    // log('weibo成功获取到？', weibo)
    var WeiboCell = WeiboTemplate(weibo)
    // 插入 Weibo-list
    var WeiboList = e('.weibo-list-gua-auto-list')
    WeiboList.insertAdjacentHTML('beforeend', WeiboCell)
}

var insertEditForm = function(cell) {
    var form = `
        <div class='Weibo-edit-form'>
            <input class="Weibo-edit-input">
            <button class='Weibo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('beforeend', form)
}

var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
        // console.log('load all', r)
        // 解析为 数组
        var Weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < Weibos.length; i++) {
            var Weibo = Weibos[i]
            insertWeibo(Weibo)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add-weibo')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        // log('click add', content)
        var form = {
            'content': content,
        }
        // log('form表单', form)
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            log('添加weibo成功')
            var weibo = JSON.parse(r)
            // log('var weibo = JSON.parse(r) 这一步结果？', weibo)
            insertWeibo(weibo)
        })
    })
}

var bindEventWeiboDelete = function() {
    var WeiboList = e('.weibo-list-gua-auto-list')
    // 注意, 第二个参数可以直接给出定义函数
    WeiboList.addEventListener('click', function(event){
        var self = event.target
        // log('click 删除按钮', self)
        if(self.classList.contains('weibo-delete')){
            // 删除这个 Weibo
            var WeiboCell = self.parentElement
            var Weibo_id = WeiboCell.dataset.id
            apiWeiboDelete(Weibo_id, function(r){
                log('删除weibo成功', Weibo_id)
                WeiboCell.remove()
            })
        }
    })
}

var bindEventWeiboEdit = function() {
    var WeiboList = e('.weibo-list-gua-auto-list')
    // 注意, 第二个参数可以直接给出定义函数
    WeiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('weibo-edit')){
            log('weibo-edit',self)
            // 删除这个 Weibo
            var WeiboCell = self.parentElement
            insertEditForm(WeiboCell)
        }
    })
}


var bindEventWeiboUpdate = function() {
    var WeiboList = e('.weibo-list-gua-auto-list')
    // 注意, 第二个参数可以直接给出定义函数
    WeiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('Weibo-update')){
            log('点击了 update ', self)
            //
            var editForm = self.parentElement
            // querySelector 是 DOM 元素的方法
            // document.querySelector 中的 document 是所有元素的祖先元素
            var input = editForm.querySelector('.Weibo-edit-input')
            var content = input.value
            // 用 closest 方法可以找到最近的直系父节点
            var WeiboCell = self.closest('.weibo-cell')
            // log('WeiboCell', WeiboCell)
            var Weibo_id = WeiboCell.dataset.id
            // log('Weibo_id', Weibo_id)
            // log('content', content)
            var form = {
                'id': Weibo_id,
                'content': content,
            }
            log('form', form)
            apiWeiboUpdate(form, function(r){
                // log('更新成功', Weibo_id)
                var Weibo = JSON.parse(r)
                var selector = '#weibo-' + Weibo.id
                log('selector', selector)
                var WeiboCell = e(selector)
                log('WeiboCell', WeiboCell)
                var contentSpan = WeiboCell.querySelector('.weibo-content')
                log('contentSpan', contentSpan)
                contentSpan.innerHTML = form['content']
                log('contentSpan', contentSpan)
//                WeiboCell.remove()
            })
        }
    })
}

var bindEvents = function() {
   bindEventWeiboAdd()
   bindEventWeiboDelete()
   bindEventWeiboEdit()
   bindEventWeiboUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
