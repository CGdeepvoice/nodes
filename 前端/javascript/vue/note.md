# 基础
## 插值
1. 文本
   1. {{ message }}, 定义在vue.data里
   2. 一次性插值 `<p v-once>{{ message }}</p>`,定义在标签中，当数据改变时，内容不会更新
2. 原始html  v-html
   `<p>using v-html directive: <span v-html="rawhtml"></span></p>`, 这里的rawhtml是Vue.data里的值

3. 属性 `<span v-bind:title="message"></span>`
4. js表达式 `{{ number +1 }}`, `{{ message.split('').reverse().join('')`
## 指令
1. 条件 v-if="message"
2. 循环 v-for="todo in todos" todos是vue.data的列表
3. 参数 v-bind:attribute=""， 这里attribute是参数, v-on:event="method", event也是参数
4. 动态参数 v-bind:[attributeName]="", attributeName定义在Vue.data
5. 修饰符 v-on:submit.prevent="onSubmit", 调用event.preventDefault()
6. 双向绑定， 绑定输入和输出 v-model

    ```js
    <div id="app-6">
      <p> {{ message }}</p>
      <input v-model="message">
    </div>
    var app6 = new Vue({
        el: "#app-6",
        data: {
            message: "hello"
        }
    })  
    ```
## 缩写
1. v-bind:key == :key  v-bind:[key] == :[key]
2. v-on:click == @click  `@[event]`
## 组件
1.  自定义组件Vue.component

    ```js
    <div id="app">
        <ol>
            <todo-item
            v-for='item in groceryList'
            v-bind:todo="item"
            v-bind:key='item.id'
            ></todo-item>
        </ol>
    </div>

    Vue.component('todo-item', {
        props: ['todo'],
        template: '<li>{{ todo.text }}{{ todo.id }}</li>'
    })
    var app = new Vue({
        el: "#app",
        data: {
            groceryList: [
                {id: 0, text: "蔬菜"},
                {id: 1, text: "肉"},
                {id: 2, text: "牛奶"}
            ]
        }
    })
    ```
2.  生命周期钩子函数，像信号量，当运行到某个阶段会发出信号，定义函数来响应。
3.  