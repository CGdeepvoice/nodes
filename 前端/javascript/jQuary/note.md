### jQuery
#### core
1. $ 即为jquery对象， 方法在jquery对象上进行调用,返回到this上面
2. $(document).ready(), Dom加载完成之后进行调用。
3. 符号冲突，如果其他库也使用了$， 可以替换为其他符号
   - var $x = jQuery.noConflict(); $ 替换为$x
   - jQuery.noConflict();  可以使用默认的jQuery
4. 属性 .attr(), 可以作为getter、setter
   - setter   $("a").attr('href', 'allmyHrexxx.html');
   - getter   $("aa").attr("href");
5. 选择器
   - ID  $("#Id");
   - class name   $(".myClass");
   - attribute    $("input[name='first_name']");
   - 复合选择器     $("#contents ul.people li");
   - 逗号分割选择列表 $("div.myClass, ul.people");
   - 伪类          $("a.external:first");
    1. 对结果选择和过滤
        - $("div.foo").has("p"); // div.foo elements that contain ```<p>```tags
        - $("hi").not(".bar");  // h1 elements that don't have a class of bar
        - $("ul li").filter(".current"); // unordered list items with class of current
        - $("ul li").first();  // just the first unordered list item
        - $( "ul li" ).eq( 5 );              // the sixth 索引为5 第六个
    2. 选择表单元素
        - $("form :checked);  // 选择器选取所有选中的复选框或单选按钮。
        - $("form :disabled");  // 选择有disable属性的Input元素。
        - $("form :enabled");  // 选择任何没有disabled的元素
        - $("form :input");   // input,textarea, select,button属性
6. 处理选择器
    1. Getters & Setters   作用在选择器上的一些方法可以设置和获取值， 例如
    ```js
    $("h1").html("hello world");   // 设置,选择器中所有的元素都会设置
    $("h1").html();   // 返回第一个元素的的值
    ```
    2. 链式操作
    ```js
    $("#content").find("h3").eq(2).html("new text for the third h3");
    ```
    end() 可以返回原始的选择器继续操作
    ```js
    $("#content")
        .find("h3")
        .eq(2)
            .html("new text for third h3!")
            .end()
        .eq(0)
            .html("new text for the first h3");
    ```
7. 操作元素
    1. geting and setting
        - .html()  所有元素的html contents
        - .text()  所有元素的text contents
        - .attr()  所有元素的attribute
        - .width() 第一个元素的宽度
        - .height() 第一个元素的高度
        - .position() 第一个元素的位置（相对于父节点）
        - .val()  获取表单元素的值
    2. move
        - .insertAfter()  将选择的元素放置到参数元素之后
        - .insertBefore()
        - .appendTo()
        - .prependTo()  前置
        - .after()  将参数的元素放到所选择元素之后
        - .before()
        - .append()
        - .prepend()

    ```js
    var li = $("#myList li:first").appendTo("#myList");
    $("#myList").append($("#myList li:first"));
    // 作用相同，第一种有返回值，把第一个放到最后一个
    ```
    3. copy
        - .clone() 
        ```js
        $("#myList li:first").clone.appendTo("myList");
        ```  
    4. remove
        - .remove() remove和detach都会返回这个元素并删除，区别在于， remove删除这个元素上绑定的方法和属性，重新加回去方法和属性消失，detach会保存
        - .detach()
        - .empty() 清空内容

    5. create
   
        ```js
            $( "<p>This is a new paragraph</p>" );
            $( "<li class=\"new\">new list item</li>" );
            $( "<a/>", {
                html: "This is a <strong>new</strong> link",
                "class": "new",
                href: "foo.html"
            });
        ```

    6. 操作属性 .attr()
       - 直接修改赋值
       - 创建回调函数，包含两个参数，一个是更改属性元素的索引和更改属性的当前值
8. 遍历
   1. Parents
        - .parent() 直接父节点
        - .parents() 父节点，包含父节点的父节点...
        - .parentsUntil()  父节点直到，不包含里面的选择器
        - .clsest()  最近的
        ```js
        // returns [ div.child ]
        $( "span.subchild" ).parent();

        // Selecting all the parents of an element that match a given selector:
        // returns [ div.parent ]
        $( "span.subchild" ).parents( "div.parent" );

        // returns [ div.child, div.parent, div.grandparent ]
        $( "span.subchild" ).parents();
        
        // Selecting all the parents of an element up to, but *not including* the selector:
        // returns [ div.child, div.parent ]
        $( "span.subchild" ).parentsUntil( "div.grandparent" );
        
        // Selecting the closest parent, note that only one parent will be selected
        // and that the initial element itself is included in the search:
        
        // returns [ div.child ]
        $( "span.subchild" ).closest( "div" );
        
        // returns [ div.child ] as the selector is also included in the search:
        $( "div.child" ).closest( "div" );
        ```
    1. Children
        - .children()
        - .find()
    2. Siblings 兄弟节点
        - .prev() 前一个
        - .next() 后一个
        - .siblings() 前一个和后一个
        - .nextAll()
        - .nextUntil()
        - .prevAll()
        - .prevUntil()
9.  css
    1. .css() 获取和设置
    2. 对类进行操作从而对属性的修改
       - .addClass() 
       - .removeClass()  
       - .toggleClass() 切换, 如果没有就设置，如果有就删除
       - .hasClass()
    3. 尺寸
       - .width()
       - .height()
10. 数据
    1.  .data()  存放在元素上，设置和获取
11. 实用方法
    1. $.trim(） 删掉左右两边多余的空格
    2. $.each([], function(){});  遍历然后方法运行
    3.  $.inArray(idx, myArray);  获取第几个元素（索引）,找不到为-1
    4. $.extend(myArray1, myArray2); 合并，更改第一个数组并返回合并后的， 如果不想更改第一个可以传一个空进去 {}
    5. proxy 接受一个已有的函数，并返回一个带有特定上下文的新函数，通常用于向上下文指向不同对象的元素添加事件。
    6. type
        - $.isArray([]); //true
        - $.isFunction(function(){}); //true
        - $.isNumric(3.14); // true
        - $.type() 返回类型 typeof
    7. map 处理数组中的每个元素并将结果封装成新的数组返回
        - $.map(myArray, function(){})
        - $().map(function(index, element){})
    8. index(), 返回索引值，默认相对于父节点，可以见参数，字符串或者jQuery选择器结果，则索引为相对于所选对象。

#### 事件
1. DOM事件可以使用简单的方法，比如 .click(), .focus(), 可以替换为.on()方法，第一个参数为事件名，例如 .on('click', callback)
2. .on() 只能绑定到在定义整个事件时候已经存在的元素，如果先定义了监听事件，但此时元素不存在，这是创建元素也不会响应事件
3. event参数，每个监听事件都会有一个event参数，下面为event对象的常用属性和方法
   - pageX, pageY 事件发生时的鼠标位置，相对于页面显示区域的左上角
   - type  事件类型，比如click
   - which 按下的Button or key
   - data 绑定事件时候传入的参数， 比如
    ```js
    $("input").on(
        "change",
        {foo:"bar"},
        function(eventObject){
            console.log("An input value has change!", eventObject.data.foo)
        }
    )
    ```
   - target 响应事件的dom元素
   - linktimeStamp 时间戳（事件发生时候与1970-1-1的毫秒差）
   - preventDefault()  阻止默认的行为
   - stopPropagation()  停止冒泡传播
   - $(this)  表示绑定的dom元素
   - 绑定多个事件， 1. ```$("a").on('click change', function(){})``` 2. ```$("a").on({click: function(){}, mouseover: function(){}})
   - 命名空间，多人协作，可以把多个事件绑定到一个命名空间进行管理
    ```js
    // Namespacing events
    $( "p" ).on( "click.myNamespace", function() { /* ... */ } );
    $( "p" ).off( "click.myNamespace" );
    $( "p" ).off( ".myNamespace" ); // Unbind all events in the namespace
    ```
   - 删除事件， .off("click", func) ，可以删除该元素的全部事件，或者指定事件， 或者命名空间的事件。
   - 只运行一次的事件， .once()
4. 事件触发  .trigger('click')

#### 特效
1. .show() .hide(),通过修改 css的display为none， 长宽为0。参数为速度 'slow', 'normal', 'fast' 或者数值表示毫秒
2. 淡入淡出,
   - slideUp(1000) 向上慢慢淡出，然后隐藏，效果同hide
   - slideDown(1000) 慢慢显示出隐藏的内容
   - fadeOut(1000)  隐藏 同hide
   - fadeIn(1000)  显示隐藏内容
3. 切换 .toggle(),  可见变为不可见，不可见变为可见
4. 动画完成之后执行语句 ```$("p.hidden").fadeIn(1000).addClass("lookAtMe");
5. 管理特效  
    - stop() 终止特效
    - delay() 延迟
#### AJAX
1. $.ajax(), 参数:
    - async  异步 默认是true，如果设置为false则请求会阻塞其他操作
    - cache  使用缓存，默认为true
    - done  回调函数
    - fail  失败的回调
    - always  回调函数无论成功还是失败
    - url 地址
    - type  请求方法
    - data 发送的数据
    - dataType 期望返回的类型


    ```js
    // Using the core $.ajax() method
    $.ajax({
    
        // The URL for the request
        url: "post.php",
    
        // The data to send (will be converted to a query string)
        data: {
            id: 123
        },
    
        // Whether this is a POST or GET request
        type: "GET",
    
        // The type of data we expect back
        dataType : "json",
    })
    // Code to run if the request succeeds (is done);
    // The response is passed to the function
    .done(function( json ) {
        $( "<h1>" ).text( json.title ).appendTo( "body" );
        $( "<div class=\"content\">").html( json.html ).appendTo( "body" );
    })
    // Code to run if the request fails; the raw request and
    // status codes are passed to the function
    .fail(function( xhr, status, errorThrown ) {
        alert( "Sorry, there was a problem!" );
        console.log( "Error: " + errorThrown );
        console.log( "Status: " + status );
        console.dir( xhr );
    })
    // Code to run regardless of success or failure;
    .always(function( xhr, status ) {
        alert( "The request is complete!" );
    });
    ```

2. 便捷方法
   1. $.get() 发送get请求
   2. $.post() 
   3. $.getScript() 通过AJAX请求获得并运行一个javaScript文件
   4. $.getJSON()  发送一个get请求并接受一个Json
   5. $.load()  通过ajax请求获得并改变div元素
3. 处理表单
   1. serialization 序列化
        - .serialize() 将表单内容序列化为 query string (field1=1&field2=2)
        - .serializeArray() 序列化为数组
   2. 客户端验证 .submit(function(event){//进行验证})
   3. ajaxPrefilter 用于指定预先处理Ajax参数选项的回调函数。