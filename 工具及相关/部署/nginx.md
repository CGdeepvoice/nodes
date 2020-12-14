# nginx
支持http和反向代理的高性能的web服务器。

1. 反向代理

![avator](images/反向代理.png)

正向代理中，proxy和client同属一个LAN，对server透明；
反向代理中，proxy和server同属一个LAN，对client透明。
实际上proxy在两种代理中做的事都是代为收发请求和响应，不过从结构上来看正好左右互换了下，所以把后出现的那种代理方式叫成了反向代理

2. web服务器

指长期驻留与因特网的某种类型的计算机程序，可以处理客户端的请求，并返回响应。可以防止网站，让其他人浏览。可以防止数据，让其他人下载。

## 架构

目录： /usr/local/opt/nginx/bin
    启动： ./nginx
    停止： ./nginx -s stop/quit
    重启: ./nginx -s reload
查看进程 ps -ef | grep nginx
配置文件： /usr/local/etc/nginx/nginx.conf

![avator](images/nginx架构.jpg)

1. 进程模型

    主进程和多个工作进程，master、worker进程。主进程负责工作调度，负责加载配置、启动worker进程和热更新。所以说最少两个nginx进程。worker负责处理网络请求，每个worker可以处理数以千计的网络请求。

    为什么一个worker可以支持上万的并发量呢？
    异步非阻塞 + epoll事件驱动

    **同步、异步、阻塞、非阻塞**

    [同步、异步、阻塞、非阻塞](https://www.jianshu.com/p/aed6067eeac9)

    同步: 一个任务A依赖任务B，只有任务B完成，任务A才算完成。
    异步：任务A执行过程中，调用任务B，结束任务A，等待通知

    阻塞：在任务B执行过程中，A不能做别的，一直等待。
    非阻塞：在任务B完成过程中，可以做别的

    同步阻塞：小明在银行排队等叫号。等待过程中一直看着叫号器。
       
       这里的同步体现在，小明在等待叫号
       这里的阻塞体现在，小明在等待的过程中什么都不做
    
    同步非阻塞：小明在等待过程中，可以一边玩手机，一边看叫号器。

        同步体现在， 小明在等待叫号
        非阻塞体现， 一边玩手机，一边等待。等待过程中做其他的。
    
    异步阻塞：小明告诉大堂经理，到了给我打电话，然后小明去外面等着电话。

        异步体现在：小明不等待叫号，等着通知（回掉函数）
        阻塞体现在：结束了当前的等叫号任务，但是还是没做其他的。
    
    异步非阻塞：小明告诉大堂经理，到了给我打电话，小明去外面吸烟玩手机。

        异步体现在：小明不等待叫号，等着通知（回掉函数）
        非阻塞体现在：可以做别的事情

    select vs epoll
    select 线程持有很多fd，遍历所有找到完成的进行通信。
    epoll 注册任务，等待完成之后在进行处理。

2. 模块化

    worker包含核心模块和功能模块。核心模块肤色一个运行循环，run-loop。执行网络请求处理的不同阶段的模块功能，网络读写，存储读写，内容传输，以及将请求发送到上游服务器。


3. 常用配置
   
   nginx.conf

```bash
worker_process 1;       # worker进程数
events {                # 事件的配置
    worker_connections 1024;    # worker的最大连接数
}

http {          # http请求的配置
    include         mime.types; # 引入了mime.types文件
    default_type    application/octet-stream;   # 请求响应的默认数据类型

    sendfile        on;     # 启用sendfile，在底层拷贝数据的时候可以跳过应用，直接从内核拷贝到网卡，加快速度
    keepalive_timeout 65;   # 一个长连接的存活时间，一个连接的三次握手完成之后，发送请求，一个请求结束不会立即挥手，而是等有无其他请求。
    
    server {        # 配置一个虚拟机
        listen      8080;   # 监听的端口号
        server_name localhost;  # 配置域名，分发请求的时候根据访问的域名和配置的域名的对应关系进行分发

        location / {    # 一个请求地址，这里可以使用正则匹配
            root    html;       # root表示页面所在的目录  这里的html是nginx目录中的html文件，也可以指定到其他位置，或者链接过来
            index   index.html index.htm;
        }
    }
}
```

动静分离，static -> images/js/css 

```bash
localtion /static {
    alias html/static/;
}
访问时候 url/static/**.jpg
```
**正则**
```bash
location = /uri 表示精准匹配，完全相等
location ^~ /uri  前缀匹配
location ~ pattern  区分大小写的正则匹配
location ~* pattern 不区分大小写的正则
location /uri 前缀匹配，在正则匹配之后
location / 通用匹配
```

```bash
localtion ~*\.(jpg|png|git|css|js)$ {
    root /Users/chenge/data/images;
}
```

**防倒链**
```bash
localtion ~*\.(jpg|png|git|css|js)$ {
    root /Users/chenge/data/images;
    valid_referers none blocked *.test.com;  # 只允许test.com域名访问图片，其他的就是403

    if ($invalid_referer){
        return 403;
    }
}
```

**黑白名单配置**
黑名单
nginx.conf
```bash
http {
    include black.ip;
}
```
创建black.ip 文件，添加 `deny 192.11.1.1`要拉黑的ip.直接返回403

白名单
write.ip `192.168.128.123 1`
nginx.conf
```bash
http {
    geo $remote_addr $ip_whitelist {
        default 0;
        include white.ip;
    }

    server {
        listen 8080;
        server_name localhost;

        location / {
            if ($ip_whitelist = 0){
                return 403;
            }
            root html;
            index index.html;
        }
    }
}
```
geo引入了白名单，默认值都是0，然后引入自定义的ip，为1.在location是判断，如果是0就403

**网络限速**
这里是限制传输速度，不是连接总数。
```bash
server {
    listen 80;
    server_name test.com;
    location ~*\.(jpg|png|gif)$ {
        root html/static;

        limit_rate 1k;  # 如果开始限速，限速为1k下载速度
        limit_rate_after 2k; # 小于2k的部分不限速

        valid_referers *.test.com;
        if ($invalid_referer){
            return 403;
        }
    }
}
```

**限流配置**
令牌桶限流，令牌以固定的速度产生，放到令牌桶，令牌桶满了之后就丢弃多余的令牌。请求要消耗令牌，没有令牌等待。

漏桶算法 突发流量会进入漏桶，漏桶以固定的速率处理请求，如果水流过大也就是突发流量过大，就会溢出，多余的请求被拒绝。

两者的区别就是令牌桶可以允许一定的突发流量

limit_req_zone 显示单位时间内的请求数量，速率限制，使用漏桶算法 leaky bucket
limit_req_conn 同一时间的连接数，并发限制

**日志配置**
两部分，日志合格和日志级别位置。
```bash
http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                     '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  logs/access.log  main;
```
复制access.log到access_bak.log,新建access.log需要reopen操作。nginx -s reopen

1. 反向代理

proxy_pass
```bash
location = /baidu.html {
    proxy_pass http://www.baidu.com;
}
```

5. 负载均衡

    proxy_pass可以把请求代理至后端服务，为了实现更高的负载和性能，后端服务通常是多个，使用Upstream来进行负载均衡

```bash
http {
    upstream wwwdemocom {
        server 127.0.0.1:8080 weight=1;
        server 127.0.0.1:8090 weight=2;
    }

    server {
        listen 80;
        server_name www.demo.com;

        location / {
            proxy_pass http://wwwdemocom;
        }
    }
}

```
upstream参数：
 1. service 反向服务地址加端口
 2. weight 权重
 3. max_fails 失败多少次认为主机已经挂掉，提出
 4. fail_timeout 提出后重新探测时间
 5. backup 备用服务
 6. max_conns 允许最大连接数

**负载均衡算法**
  1. ll + weight  轮询加权重 默认。 
  2. ip_hash 可以保持session一致性，对ip进行hash计算，分发到固定的主机
  3. url_hash 静态资源缓存
  4. least_conn 最少连接，把请求优先分给nginx连接最少的主机。
  5. least_time 响应时间最快

6. 缓存

    静态缓存，nginx优先访问本地文件缓存，如果没有再继续请求
    可以通过配置http中的proxy_cache_path缓存地址和inactive有效期添加缓冲区。在location中配置proxy_cache来指定缓存。这样会在本地文件中缓存静态网页

    缓存更新，不能一直缓存，在数据更新时候需要更新缓存，使用第三方模块 ngx_cache_purge来实现。

7. 高可用

也就是当nginx服务器挂了，那所有服务都无法使用了。可以使用软件keepalived,设置备份服务器，主从之间心跳检测，如果主服务器挂了，备份服务器就开始生效。

nginx

8. 其他设置
  sendfile: 不启用的话， 硬盘——> 内核缓冲 ——> 用户缓冲  ——> socket缓冲 ——> 协议栈
            启用的话: 硬盘 ——> 内核缓冲（拷贝到socket缓冲) ——> 协议栈
            不需要用户态和内核态的切换。
  tcp_nopush: 当发送包的时候，不会立刻发送，而是等到数据包最大的时候一次性传输过去，有助于解决网络拥堵。
  tcp_nodelay: 不用等待前一个包的ack就能发送，这两个并不矛盾