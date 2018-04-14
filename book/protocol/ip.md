# IP协议

## IP地址分类

> IPv4 地址分为 4个类别, A类、B类、C类、D类

**A类地址**

`0.0.0.0 ~ 127.0.0.0`

**B类地址**

`128.0.0.0 ~ 191.255.0.0`

**C类地址**

`192.0.0.0 ~ 223.255.255.0`

**D类地址**

`224.0.0.0 ~ 239.255.255.255`

## ping 命令

> ping 检查网络是否连通

```bash
ping csdn.net

PING csdn.net (47.95.164.112): 56 data bytes
64 bytes from 47.95.164.112: icmp_seq=0 ttl=35 time=35.833 ms
64 bytes from 47.95.164.112: icmp_seq=1 ttl=35 time=37.213 ms
64 bytes from 47.95.164.112: icmp_seq=2 ttl=35 time=88.710 ms
64 bytes from 47.95.164.112: icmp_seq=3 ttl=35 time=33.389 ms
```

## traceroute 命令

> traceroute 路由追踪

```bash
traceroute csdn.net


traceroute to csdn.net (47.95.164.112), 64 hops max, 52 byte packets
 1  192.168.31.1 (192.168.31.1)  41.530 ms  1.268 ms  1.037 ms
 2  192.168.1.1 (192.168.1.1)  1.672 ms  1.995 ms  2.720 ms
 3  10.96.0.1 (10.96.0.1)  5.581 ms  5.305 ms  48.190 ms
 4  111.0.92.225 (111.0.92.225)  7.064 ms  10.488 ms  6.935 ms
```