## html
### 基础
1. 块级元素和内联元素，块级元素会出现在新的一行
2. 空元素，只有一个标签来表示插入一些东西，例```<img>```，不需要关闭
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
1. 图片， ```<img src="服务器相对地址或者网址" alt="对图片文字描述，图片无法显示时候" title="悬停时显示">```
2. 音频和视频 video audio
3. 嵌入其他内容，iframe
4. 矢量图： 包含图形和路径的定义，svg格式，放大不失真； 位图：每个像素的位置和色彩信息，放大后会失真
### 表格
    - table标签
    - caption 标题
    - tr table row 一行标签
    - td table data 具体的单元格内容
    - th 可替换td,作为表头，table header, 
    - 属性包含： rowspan 跨几行， colspan 跨几列
    - colgroup 放在table开始处，可以为每列设置属性，包含col标签，数量与正常列相同（可以使用span）
### 表单
1. form:
   - action: url
   - method: HTTP method
2. 基础部件 widget：
    - label 属性for，指向对应部件的id, 点击标签可以激活相应部件
    - input type 类型 提交时候会进行校验 value默认值，placeholder背景字
    - 自动补全输入框， datalist-> option, input list属性关联到datalist id
    - 可选框
        - 单选框  ```<input type="radio">```
        - 复选框  ```<input type="checkbox">```
    - textarea
    - select 选择框， select -> option, 多选框：multiple属性
    - button
        - submit 将表单数据发送到服务器。
        - reset 将所有表单小部件重新设置为它们的默认值。
        - anonymous 没有自动生效的按钮，但是可以使用JavaScript代码进行定制。
    - fieldset, lengend标签
        ```<fieldset>元素是一种方便的用于创建具有相同目的的小部件组的方式，出于样式和语义目的。 你可以在<fieldset>开口标签后加上一个 <legend>元素来给<fieldset> 标上标签。 <legend>的文本内容正式地描述了<fieldset>里所含有部件的用途。```
3. 高级部件
   - 数字 ```<input type="number" name="age" id="age" min="1" max="10" step="2">```
   - 滑块 ```<input type="range" name="beans" id="beans" min="0" max="500" step="10">```
   - 日期时间选择器 ```<input type="datetime-local" name="datetime" id="datetime">``` 支持min,max
        - 本地时间 type="datetime-local"
        - 月 type="month"
        - 时间 type="time"
        - 星期 type="week"
    - 文件选择器 ```<input type="file" name="file" id="file" accept="image/*" multiple>```
    - 隐藏内容 type="hidden"
    - 图像按钮 type="image"
    - 进度条和仪表  progress meter
4. 部件通用属性(表单)
   
属性 | 默认值 | 描述
:-:|:-:|:-: 
autofocus | flase | 自动具有输入焦点，只有一个可以设置
disabled | false | 不能与元素交互
name | | 元素的名称;这是跟表单数据一起提交的。
value | | 元素的初始值。