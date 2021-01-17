# 介绍
angular js是一个js框架，通过指令的方式扩展了HTML

## 指令
1. ng-app 定义一个Angularjs 应用程序，用来表示这个元素是angular js应用程序的所有者
2. ng-model 将元素值 如输入区域的值 绑定到应用程序，把输入绑定到应用程序的变量
3. ng-bing 吧应用程序数据绑定到html视图，也可以使用插值表达式来插入，用来展示应用程序的变量值
4. ng-init 用来初始化应用程序的变量

```js
<div ng-app="" ng-init="firstName='John'">
    <p>姓氏为: <input type="text" ng-model="firstName"></p>
    <p>Hello, {{firstName}}</p>
    <p ng-bind="firstName"></p>
</div>
```
5. 插值表达式 `{{expression}}`
6. 模块 module 定义AngularJs应用  `var app = angular.module('myApp', []);`
7. 控制器Controller 用于控制Angularjs应用 

```html
<div ng-app="myApp" ng-controller="myCtrl">
    姓：<input type="text" ng-model="firstName">
    名：<input type="text" ng-model="lastName">
    <br/>
    姓名: {{firstName + " " + lastName}}
</div>

<script>
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope) {
    $scope.firstName="John";
    $scope.lastName="Doe";
})
</script>
```
8. ng-repeat 重复一个html元素

```html
<div ng-app="" ng-init="names=['jani', 'hege', 'kai']">
    <ul>
        <li ng-repeat="x in names">
        {{ x }}
        </li>
    </ul>

</div>
```
9. ng-show 当表达式为true的时候显示该元素
10. 表单验证， `{{myForm.myAddress.$valid}}`,这里有 invalid表示输入是否合法，dirty值改变，touched通过触屏点击， error错误信息，是一个对象，通过`<span ng-show="myForm.myAddress.$error.email">不是一个合法的邮箱地址</span>`
可以通过状态也修改css.
11. Scope 作用域，创建控制器，可以将 `$scope`作为参数传递。

    angularjs应用由三部分组成： view视图，即html. model模型，当前视图中可用的数据。Controller控制器，即js函数，可以添加和修改属性。
    其中scope就是模型，是一个js对象，带有属性和方法，可以在视图和控制器中使用。
    html dom中有多个作用域。所有的应用都有一个`$rootScope`，可以通过ng-app指令包含到所有的html元素中。

12. 过滤器，使用管道符添加到表达式和指令中。可以自定义过滤器， `app.filter('fn', function(){})`

13. service服务，可以通过内置的服务获取信息

```js
var app = angular.module('myApp', []);
app.controller('customersCtrl', function($scope, $location) { 
    $scope.myUrl = $location.absUrl();// 通过$location获取当前的url
});
app.controller('myCtrl', function($scope, $http) {
    $http.get("welcome.htm").then(function (response) {
        $scope.myWelcome = response.data; // 使用$http服务进行发送请求
    });
});
```
14. 事件    ng-click点击事件
15. 路由
