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