## html
### 基础
1. 块级元素和内联元素，块级元素会出现在新的一行
2. 空元素，只有一个标签来表示插入一些东西，例```<img>```
3. head 头部信息
    1. title
    2. 元数据 ```<meta>``` 描述数据的数据
        - charset 字符编码，一般为utf-8
        - name,content name表示包含元素类型，content为值,例 ```<meta name="author" content="Chris Mills">```
    3. link
        - 自定义图标, 保存在与网站的索引页面相同的目录中,```<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">```
        - 引入css  ```<link rel="stylesheet" href="my-css-file.css">```
4. script, 引入js代码，```<script src="my-js-file.js"></script>``` 放在尾部
5. 列表
    - 无序列表， ul
    - 有序列表， ol
6. 强调 ```<em>```， 斜体 ```<i>``` 表达外国文字、分类名称、技术术语、思想等
7. 重要```<strong>``` ， 粗体 ```<b>``` 表达关键字、产品名称等
8. 超链接 ```<a herf="跳转的地址" title="鼠标悬停出现的提示">```
9. 描述列表 ```<dl><dt><dd></dd></dt></dl>``` 
    - dl: description list
    - dt: description terms
    - dd: description description
10. 引用
    - blockqute 块引用 
    - q 行内引用 
    - cite属性，不显示，用url指向引用的资源
11. 缩略语 abbr 属性：title
12. 联系方式 address
13. 时间和日期 ```<time datetime="2016-01-20">2016年1月20日</time>```
14. 基本组成部分：
    - header  页眉
    - nav 导航
    - main 主要内容， 子区域可以是article、section、div
    - aside 侧边栏
    - footer 页脚
    - 无语义元素： 块级div, 内联span
15. 换行和水平分割线 br hr
### 多媒体与嵌入