import socket 

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
SERVER = socket.gethostbyname("www.google.com")
print(SERVER)
# client.connect(("example.com",80))