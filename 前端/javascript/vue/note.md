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

## 计算属性与监听器

```js
<div id="example">
    <p>{{ reversedMessage }}</p>
    <p>{{ reversedMessage2() }}</p>
</div>

var vm = new Vue({
    el: "#example",
    data: {
        message: "hello"
    },
    methods: {
        reversedMessage2: function(){
            return this.message.split("").reverse().join("")
        }
    },
    computed: {
        reversedMessage: function(){
            return this.message.split("").reverse().join("")
        }
    }
})
```
1. 计算属性是computed， 方法是methods, 结果是相同。
  
    区别，computed是带缓存的，如果依赖项没有改变不会再次计算。methods是每次都会重新运行
2. computed setter

    ```js
    computed: {
        fullName: {
            get: function(){
                return this.firstName + " " + this.lastName
            },
            set: function(newValue){
                var names = newValue.split(' ')
                this.firstName = names[0]
                this.lastName = name[names.leng-1]
            }
        }
    }
    ```
    当对vm.fullName重新赋值时候调用setter

3. 侦听属性 watch
    watch来侦听data.property
    ```js
    <div id="demo">{{ fullName }}</div>
    var vm = new Vue({
        el: '#demo',
        data: {
            firstName: 'Foo',
            lastName: 'Bar',
            fullName: 'Foo Bar'
        },
        watch: {
            firstName: function (val) {
            this.fullName = val + ' ' + this.lastName
            },
            lastName: function (val) {
            this.fullName = this.firstName + ' ' + val
            }
        }
    })
    ```

## class style
1. 对象     `<div v-bind:class="{ active: isActive }"></div>`
            `<div v-bind:class="classObject"></div>`
2. 数组    `<div v-bind:class="[avtiveClass, errorClass]"></div>`

## 条件渲染
1. v-if v-else-if v-else
2. v-show  false则设置display=false
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