import socket

# 创建套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接服务器
client_socket.connect(('127.0.0.1', 8080))
# 发送数据
client_socket.send('i am client'.encode('utf-8'))
# 接收数据
data = client_socket.recv(1024)
print(data.decode('utf-8'))
# 关闭套接字
client_socket.close()