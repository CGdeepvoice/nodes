### 基础
1. 导入
   - 在head中添加 ```<link href="styles/style.css" rel="stylesheet">```
   - 在head中添加 ```<style></style>```
2. 选择器


名称 | 选择的内容 | 示例
:-: | :-: | :-: 
元素选择器 | html元素 | p
id 选择器 | 具有特定id的元素  | #my-id
类选择器  | 具有特定类的元素 | .my-class
属性选择器 | 具有特定属性的元素 | img[src]
伪类选择器  | 特定状态下的特定元素 | a.hover 鼠标悬停在a标签上时

使用：
    - 元素选择器 ```a.id```
    - 元素，元素 a, p   a和p
    - 元素 元素  ul li   li在ul内部
    - 元素 + 元素 h1 + p   h1和相邻的一个p元素
    - 规则： @rules
        - ```@import 'styles2.css'```
        - ```@media(min-width: 30em){body {color: "blue"}}```  媒体查询， 当浏览器宽度小于30em, 则显示蓝色
 
速记属性： font, background, padding, border, margin 等，可以在一行设置多个值
例如： padding: 10px 15px 15px 5px;  top right bottom left

### 构建css
#### 1. 层叠与继承

1. 层叠 当应用两条同级别的规则到一个元素的时候，写在后面的就是实际使用的规则。
2. 优先级 一个元素选择器不是很具体 — 会选择页面上该类型的所有元素 — 所以它的分数就会低一些
   - 内联 > ID选择器 > 类选择器=属性选择器=伪类 > 元素、伪元素选择器
   - !important 加载属性值后面 表示此个属性优先级最大

3. 继承 一些设置在父元素上的css属性是可以被子元素继承的，有些则不能。
   控制继承（属性值）：
    - inherit 开启继承
    - initial 设置属性值和浏览器默认样式相同。如果浏览器默认样式中未设置且该属性是自然继承的，那么会设置为 inherit 。
    - unset 将属性重置为自然值，也就是如果属性是自然继承那么就是 inherit，否则和 initial一样