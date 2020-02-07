# import socket

# soc = socket.socket()
# soc.connect(('localhost',5000))
# savefilename = input("enter file name to receive: ")

# while True:
#         recvfile = soc.recv(4096)
#         if not recvfile: break
#         openfile = open(savefilename, 'wb')
#         file.write(recvfile)
#         print("File has been received.")
    
# soc.close()

# import socket

# soc = socket.socket()
# soc.connect(('localhost',8080))
# savefilename = input("enter file name to receive: ")
# file=open(savefilename,'rb')
# print(file)
# while True:
#         recvfile = soc.recv(4096)
#         print(recvfile)
#         if not recvfile: break
#         file.write(recvfile)
#         print("File has been received.")
# soc.close()


import socket
soc = socket.socket()
soc.connect(('localhost',8080))

savefilename = input("enter file name to receive: ")
with soc,open(savefilename,'wb') as file:
    while True:
        recvfile = soc.recv(4096)
        print(recvfile)
        if not recvfile: break
        file.write(recvfile)
print("File has been received.")
