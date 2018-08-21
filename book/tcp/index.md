# TCP协议

通过IP数据报实现可靠性传输需要考虑很多问题
例如:
    - 数据的破坏
    - 丢包
    - 重复
    - 分片顺序混乱

TCP设计:
    - 校验和
    - 序列号
    - 确认应答
    - 重发控制
    - 连接管理
    - 窗口控制


## TCP报文格式

![](./_image/2018-03-26-22-30-08.png)

- 源端口号 Source Port : 表示发送端端口
- 目标端口号 Destination Port : 表示接收端端口号
- 序列号 Sequence Number : 发送数据的位置
- 确认应答号 Acknowledgement Number : 表示已接收到 应答号减一为止的数据
- 数据偏移 Data Offset : TCP首部长度
- 保留 Reserved : 该字段主要为了以后扩展用
- 控制位 Control Flag
    - CWR : 与拥塞窗口相关
    - ECE
    - URG
    - ACK
    - PSH
    - RST
    - SYN
    - FIN
- 窗口大小 Window Size : 一次可以发送数据的大小
- 校验和 Checksum : 数据完整性校验
- 紧急指针 Urgent Pointer :



## TCP连接的建立与终止

- 时间序列
- 建立连接
- 建立连接超时
- 最大报文段长度 MSS
- TCP的半关闭
- TCP的状态变迁
    - 2MSL等待状态
    - 平静时间的概念
- 复位报文段 RST
- 同时打开
- 同时关闭
- TCP选项
- TCP服务器的设计



## TCP的交互数据流

## TCP的成块数据

## TCP的超时重传

## TCP的定时器

## TCP的未来与性能
