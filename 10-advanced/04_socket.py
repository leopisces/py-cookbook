"""
网络编程 (Socket Programming)
=================================
Python socket 网络编程: socket 创建、TCP 客户端/服务端(用 localhost 演示)、
UDP 概念、简单 echo 服务示例。

参考: https://www.runoob.com/python3/python3-socket.html
"""

import socket
import threading
import time


# ========== 演示 1: socket 基础知识 ==========
def demo_socket_basics():
    """了解 socket 的基本概念和创建方法"""
    print("=" * 50)
    print("演示 1: Socket 基础知识")
    print("=" * 50)

    print("""
  Socket (套接字) 是网络通信的端点。

  常见协议族:
    AF_INET  - IPv4 地址 (最常用)
    AF_INET6 - IPv6 地址
    AF_UNIX  - Unix 域套接字 (本机进程间通信)

  常见 Socket 类型:
    SOCK_STREAM - TCP 协议 (面向连接、可靠)
    SOCK_DGRAM  - UDP 协议 (无连接、不可靠但快速)

  通信流程:
    TCP 服务端: socket() → bind() → listen() → accept() → recv()/send()
    TCP 客户端: socket() → connect() → send()/recv()
    """)

    # 创建一个 TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"  TCP Socket 创建: {tcp_socket}")
    print(f"  地址族: {tcp_socket.family} (AF_INET)")
    print(f"  类型: {tcp_socket.type} (SOCK_STREAM)")
    tcp_socket.close()

    # 创建一个 UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"\n  UDP Socket 创建: {udp_socket}")
    print(f"  地址族: {udp_socket.family} (AF_INET)")
    print(f"  类型: {udp_socket.type} (SOCK_DGRAM)")
    udp_socket.close()

    # 查看常用的 socket 函数
    print("""
  常用方法:
    bind(address)    - 绑定地址
    listen(backlog)  - 开始监听 (TCP)
    accept()         - 接受连接 (TCP, 阻塞)
    connect(address) - 连接到服务器 (TCP)
    send(data)       - 发送数据
    recv(bufsize)    - 接收数据
    close()          - 关闭 socket
  """)
    print()


# ========== 演示 2: TCP Echo 服务器 (后台线程) ==========
def demo_tcp_echo():
    """使用 TCP 实现简单的 Echo 服务器和客户端"""
    print("=" * 50)
    print("演示 2: TCP Echo 服务 (客户端发送 -> 服务端回显)")
    print("=" * 50)

    HOST = "127.0.0.1"
    PORT = 0  # 让操作系统自动分配端口

    server_ready = threading.Event()
    actual_port = [None]
    server_thread = [None]

    def run_server():
        """TCP Echo 服务器 - 接收并回显数据"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            actual_port[0] = s.getsockname()[1]
            s.listen(1)
            s.settimeout(2)  # 超时防止永久阻塞
            print(f"  [服务端] 启动于 {HOST}:{actual_port[0]}")
            server_ready.set()

            try:
                conn, addr = s.accept()
                print(f"  [服务端] 收到连接: {addr}")
                with conn:
                    # 接收客户端数据并回显
                    data = conn.recv(1024)
                    print(f"  [服务端] 收到: {data.decode()}")
                    # 回显: 把收到的数据原样发回去
                    response = f"Echo: {data.decode()}"
                    conn.sendall(response.encode())
                    print(f"  [服务端] 已回显")
            except socket.timeout:
                print("  [服务端] 等待连接超时")
            except Exception as e:
                print(f"  [服务端] 异常: {e}")

    def run_client(port):
        """TCP Echo 客户端 - 发送数据并接收回显"""
        # 等待服务端就绪
        server_ready.wait()
        time.sleep(0.3)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"  [客户端] 连接到 {HOST}:{port}")
            s.connect((HOST, port))

            # 发送消息
            message = "你好，世界！"
            s.sendall(message.encode())
            print(f"  [客户端] 发送: {message}")

            # 接收回显
            response = s.recv(1024)
            print(f"  [客户端] 收到回显: {response.decode()}")

    # 启动服务端线程
    server_thread[0] = threading.Thread(target=run_server, daemon=True)
    server_thread[0].start()

    # 等待服务端启动后再运行客户端
    server_ready.wait()
    run_client(actual_port[0])

    # 等待服务端线程结束
    server_thread[0].join(timeout=3)
    print()


# ========== 演示 3: UDP 通信概念 ==========
def demo_udp():
    """UDP 通信的基本概念演示"""
    print("=" * 50)
    print("演示 3: UDP 通信概念")
    print("=" * 50)

    print("""
  UDP (User Datagram Protocol) 用户数据报协议:

  特点:
    - 无连接: 不需要建立连接，直接发送数据
    - 不可靠: 不保证数据到达、不保证顺序
    - 速度快: 没有连接建立和确认的开销
    - 面向报文: 保留消息边界

  适用场景:
    - 实时视频/音频流
    - DNS 查询
    - 在线游戏
    - 广播/组播

  TCP vs UDP 对比:
    TCP: 可靠传输 → 文件传输、网页、邮件
    UDP: 快速传输 → 视频通话、直播、游戏
  """)

    # UDP 简单发送/接收演示
    HOST = "127.0.0.1"

    received_data = []

    def udp_receiver():
        """UDP 接收端"""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((HOST, 0))
            s.settimeout(1.5)
            port = s.getsockname()[1]
            received_data.append(port)
            print(f"  [UDP接收端] 监听 {HOST}:{port}")

            try:
                data, addr = s.recvfrom(1024)
                print(f"  [UDP接收端] 从 {addr} 收到: {data.decode()}")
            except socket.timeout:
                print("  [UDP接收端] 接收超时")

    def udp_sender(port):
        """UDP 发送端"""
        time.sleep(0.3)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            message = "UDP 测试消息"
            s.sendto(message.encode(), (HOST, port))
            print(f"  [UDP发送端] 发送到 {HOST}:{port}: {message}")

    # 启动接收线程
    receiver_thread = threading.Thread(target=udp_receiver, daemon=True)
    receiver_thread.start()
    time.sleep(0.2)  # 等待接收端绑定端口

    # 发送数据
    udp_sender(received_data[0])

    receiver_thread.join(timeout=2)
    print()


# ========== 演示 4: 多客户端 Echo 服务 ==========
def demo_multi_client():
    """使用线程实现可以处理多个客户端的 Echo 服务"""
    print("=" * 50)
    print("演示 4: 多客户端 Echo 服务")
    print("=" * 50)

    HOST = "127.0.0.1"
    PORT = 0

    server_ready = threading.Event()
    actual_port = [None]

    def handle_client(conn, addr, client_id):
        """处理单个客户端连接"""
        print(f"  [服务端] 处理客户端 {client_id} ({addr})")
        with conn:
            data = conn.recv(1024)
            print(f"  [服务端] 客户端{client_id} 发送: {data.decode()}")
            response = f"Server: 已收到 '{data.decode()}' (客户端{client_id})"
            conn.sendall(response.encode())
            time.sleep(0.05)  # 模拟处理延迟

    def run_server():
        """多客户端服务端"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            actual_port[0] = s.getsockname()[1]
            s.listen(3)
            s.settimeout(3)
            print(f"  [服务端] 启动于 {HOST}:{actual_port[0]}，可处理 3 个连接")
            server_ready.set()

            client_id = 0
            threads = []
            try:
                while client_id < 3:
                    conn, addr = s.accept()
                    client_id += 1
                    t = threading.Thread(
                        target=handle_client, args=(conn, addr, client_id), daemon=True
                    )
                    t.start()
                    threads.append(t)

                for t in threads:
                    t.join(timeout=1)
            except socket.timeout:
                pass

    def run_client(client_id, message):
        """客户端"""
        server_ready.wait()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, actual_port[0]))
            s.sendall(message.encode())
            response = s.recv(1024)
            print(f"  [客户端{client_id}] 发送: {message}")
            print(f"  [客户端{client_id}] 收到: {response.decode()}")

    # 启动服务端
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    server_ready.wait()
    time.sleep(0.2)

    # 启动多个客户端线程
    clients = [
        ("你好", 1),
        ("Hello", 2),
        ("こんにちは", 3),
    ]

    client_threads = []
    for msg, cid in clients:
        t = threading.Thread(target=run_client, args=(cid, msg), daemon=True)
        t.start()
        client_threads.append(t)

    for t in client_threads:
        t.join(timeout=2)

    server_thread.join(timeout=3)
    print()


# ========== 演示 5: socket 常用选项和技巧 ==========
def demo_socket_options():
    """Socket 常用选项和实用技巧"""
    print("=" * 50)
    print("演示 5: Socket 常用选项和技巧")
    print("=" * 50)

    print("--- 5a. SO_REUSEADDR 地址重用 ---")
    print("  允许在 TIME_WAIT 状态时重用地址，避免 'Address already in use' 错误")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"  SO_REUSEADDR 已设置")
    s.close()

    print("\n--- 5b. 设置超时 ---")
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.settimeout(5)  # 5 秒超时
    print(f"  超时时间: {s2.gettimeout()} 秒")
    s2.close()

    print("\n--- 5c. 获取本机主机名和 IP ---")
    hostname = socket.gethostname()
    print(f"  主机名: {hostname}")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"  本机 IP: {ip}")
    except socket.gaierror:
        print("  无法获取本机 IP")

    print("\n--- 5d. 域名解析 ---")
    try:
        ip = socket.gethostbyname("localhost")
        print(f"  localhost → {ip}")
    except socket.gaierror:
        print("  域名解析失败 (可能无网络)")

    print("\n--- 5e. 非阻塞模式 ---")
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s3.setblocking(False)
    print(f"  非阻塞模式已设置 (blocking={s3.getblocking()})")
    print("  非阻塞 socket 在无法立即完成操作时抛出 BlockingIOError")
    s3.close()

    print("\n--- 5f. 发送大数据的技巧 ---")
    print("""
  TCP 是流式协议，send() 不一定一次发送完所有数据:
    - 使用 sendall() 确保全部发送 (推荐)
    - 接收时注意 recv() 可能只返回部分数据
    - 协议设计: 在数据前加长度前缀，或使用分隔符

  示例模式:
    # 发送
    data = b"Hello" * 1000
    s.sendall(len(data).to_bytes(4, 'big') + data)

    # 接收
    length = int.from_bytes(s.recv(4), 'big')
    data = b""
    while len(data) < length:
        data += s.recv(length - len(data))
  """)

    print()


# ========== 主程序入口 ==========
if __name__ == "__main__":
    demo_socket_basics()
    demo_tcp_echo()
    demo_udp()
    demo_multi_client()
    demo_socket_options()
    print("\n=== 所有网络编程演示完成! ===")
