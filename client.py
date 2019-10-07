import socket
import configparser
#初始化
client = socket.socket()
ip_port = ('127.0.0.1',5678)

#连接开始
print('初始账号分别为a,b,c;密码为：1，2，3')
print('正在申请建立连接')
client.connect(ip_port)
sign = client.recv(1024)
if sign == b'sueccess' :
   print('连接服务器成功')
   while True:
     vy=input('请输入命令(输入exit可断开连接）：')
     if vy != 'exit':
      #分割字符串，提取内容
         orders =vy.split(' ')
      #发送数据
         for i in orders:
            client.send(i.encode())
            recive0 = client.recv(1024).decode()
         #输入完成
         client.send(b'finish')
         #接受反馈
         recive = client.recv(1024)
      #根据输入情况不同出现三种执行情况
         if recive == b'finish': continue
         if recive == b'Error':
             print('输入错误')
             continue
         print(str(recive.decode()))
    #断开连接
     else:
         client.send(b'exit')
         print('已断开连接')
         break
else:print('服务器无响应')