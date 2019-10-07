import socketserver
import requests
import configparser
class kv_server(socketserver.BaseRequestHandler):
      def handle(self):
          conn = self.request
          print('连接成功')
          conn.send(b"sueccess")
          #初始化
          ditionary = {}
          user_datas = {}
          Unlock = False #默认给用户权限上锁
          # 读取账号和密码
          auth = configparser.ConfigParser()
          auth.read('auth.conf')
          names = auth.options('name')
          keys = auth.options('key')
          # 存储账号密码于字典
          for i in range(len(names)):
              user_datas[names[i-1]] = keys[i-1]

          while True:
             #初始化
              data_0 = ''
              data = ['Error','Error','Error']
              i = -1
              #从用户接受命令
              while True:
                 i = i+1
                 data_0 = conn.recv(1024).decode()
                 if data_0 == 'finish' :break
                 data[i] = data_0
                 conn.send(b'sueccess')
           #判断命令类型

              if data[0] == 'SET':
                 ditionary[data[1]] = data[2]
                 conn.send(b'finish')

              if data[0] == 'GET':
                 if data[1] in ditionary:conn.send(ditionary[data[1]].encode())
                 else: conn.send(b'Error')#处理错误输入

              if data[0] == 'AUTH':
                 if (data[1] in user_datas) and (user_datas[data[1]] == data[2]):
                     Unlock=True#权限解锁
                     conn.send(b'0')

                 else:conn.send(b'-1')
              #返回文件大小
              if (Unlock) and (data[0] == 'URL'):
                  response = requests.get(data[2])
                  ditionary[data[1]] = str(len(str(response.content.decode())))
                  conn.send(str(len(str(response.content.decode()))).encode())
              #处理非法输入
              if  (data[0] != 'SET') and (data[0] != 'GET') and (data[0] != 'AUTH') and (data[0] != 'URL'):
                 conn.send(b'Error')

              if data[0] == b'exit':
                   break

#主程序
if __name__=="__main__":
    #设置默认地址，端口
    address = "127.0.0.1"
    port=5678
    print("服务端开始运行,等待连接。使用默认IP和端口")
    server = socketserver.ThreadingTCPServer((address,port),kv_server)
    server.serve_forever()