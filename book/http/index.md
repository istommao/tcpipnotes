# HTTP协议

> HTTP 超文本传输协议 是建立在 TCP协议之上的应用层协议

## HTTP报文

### 请求报文

```
<method> <request-URL> <version>
<headers>

<body>
```

`示例`

```
GET / HTTP/1.1
Host: www.github.com
Connection: Keep-Alive
```
