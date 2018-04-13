# DNS服务器

> 人类很难记忆像52.74.223.119这样的IP地址
> DNS服务的出现就是为了解决这个记忆问题
> 显然github.com这样的名字比52.74.223.11更容易记忆
> DNS就是提供这样的对应关系的解决方案


## 一些命令

```shell
dig github.com

; <<>> DiG 9.8.3-P1 <<>> github.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2864
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;github.com.            IN  A

;; ANSWER SECTION:
github.com.     600 IN  A   13.250.177.223
github.com.     600 IN  A   13.229.188.59
github.com.     600 IN  A   52.74.223.119

;; Query time: 16 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Fri Apr 13 21:17:38 2018
;; MSG SIZE  rcvd: 76
```

```shell
nslookup github.com

Server:     192.168.1.1
Address:    192.168.1.1#53

Non-authoritative answer:
Name:   github.com
Address: 13.229.188.59
Name:   github.com
Address: 52.74.223.119
Name:   github.com
Address: 13.250.177.223
```
