import socket # 导入socket模块
sever_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建一个TCP/IP套接字
sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 设置套接字选项，允许地址重用,可以快速清理缓存
# print(sever_socket) # 打印套接字对象
sever_socket.bind(('127.0.0.1', 8080)) # 绑定地址和端口
print("服务器已启动,等待客户端连接")
sever_socket.listen(5)# 监听连接，最多允许5个连接，专门接受客户端的连接请求（专门用来处理三次握手）
conn_socket, client_ip = sever_socket.accept() # 接受客户端的连接请求，返回一个新的套接字对象和客户端地址
print(client_ip) # 打印客户端地址
# print(conn_socket) # 打印新的套接字对象
recv_data = conn_socket.recv(1024) # 接收客户端的数据，最多接收1024字节
print(recv_data.decode('utf-8')) # 打印接收到的数据 
conn_socket.send('I am sever hello'.encode('utf-8')) # 发送数据给客户端 encode('utf-8')将字符串编码为字节
conn_socket.close() # 关闭连接
sever_socket.close() # 关闭套接字