from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog , QMessageBox,QApplication,QLineEdit,QInputDialog
from PyQt5.QtGui import QPixmap
from app import Ui_MainWindow
#from ss import Ui_MainWindow as form2
#from part2 import ApplicationWindow as p2
import sys
import numpy as np
import pickle
import socket
import struct
import cv2
# import cv2
# import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.btn_Game.hide()
        # self.ui.btn_Sendfile.hide()
        # self.ui.btn_Startstreaming.hide()
        self.ui.lbl_1.mouseReleaseEvent = self.showText1
        self.ui.lbl_2.mouseReleaseEvent = self.showText2
        self.ui.lbl_3.mouseReleaseEvent = self.showText3
        self.ui.lbl_4.mouseReleaseEvent = self.showText4
        self.ui.lbl_5.mouseReleaseEvent = self.showText5
        self.ui.lbl_6.mouseReleaseEvent = self.showText6
        self.ui.lbl_7.mouseReleaseEvent = self.showText7
        self.ui.lbl_8.mouseReleaseEvent = self.showText8
        self.ui.lbl_9.mouseReleaseEvent = self.showText9
        self.current = 'X'
        self.numOfClicks = 0
        self.isWiner = 0
        self.winer = ''
        self.host = "10.0.0.2"
        self.ui.ln_IP.setText(str(self.host))

        # self.text_name.setPlaceholderText('Enter your name')
        self.ui.btn_Gamestart.clicked.connect(self.StartGameConnection)
        self.ui.pushButton.clicked.connect(self.EndGameConnection)
        self.ui.pushButton_2.clicked.connect(self.ReturnBack)
        
        # self.ui.btn_Startchat.clicked.connect(self.Statchat)

        self.ui.btn_Endstreaming.clicked.connect(self.recieveStream)

        self.ui.btn_Streaming.clicked.connect(self.GoToStreamingWidget)

        self.ui.btn_Startstreaming.clicked.connect(self.SendStream)

        self.ui.btn_Back.clicked.connect(self.ReturnBack)
        self.ui.btn_Connect.hide()
        # self.ui.btn_Connect.clicked.connect(self.Connect)
        self.ui.btn_Game.clicked.connect(self.Game)
        
        self.ui.btn_Startstreaming.clicked.connect(self.SendStream)
        self.ui.btn_Recievefile.clicked.connect(self.RecieveFile)

        self.ui.btn_Sendfile.clicked.connect(self.Sendfile)
        # self.ui.btn_Startstreaming.clicked.connect(self.Startstreaming)
        self.x = 0
        self.y = 0
       ## self.ui.btn_Sendfile.clicked.connect(self.browse)


    def GoToStreamingWidget(self):
        self.ui.stackedWidget.setCurrentIndex(2)


    def EndGameConnection(self):
        self.mySocket.close()


    def ReturnBack(self):
        self.ui.stackedWidget.setCurrentIndex(0)


    def toggle(self,label):
        QApplication.processEvents()
        self.updateButtons(label)

        data = self.mySocket.recv(1024).decode()
        print('Received from server: ' + data)
        QApplication.processEvents()
        self.checkLabel(data)

    # def Statchat(self):
    #     host = self.host
    #     port = 8001


    #     mySocket = socket.socket()
    #     mySocket.connect((host,port))

    #     message = "habiba: " + input(" -> ")

    #     while message != 'q':
                
    #             mySocket.send(message.encode())
    #             data = mySocket.recv(1024).decode()

    #             print ('Received from server: ' + data)

    #             message = "habiba: " + input(" -> ")

    #     mySocket.close()
    #     print("close connection of chat")
    
    def StartGameConnection(self):
        try:
            self.port = 7000
            self.mySocket = socket.socket()
            self.mySocket.connect((self.host, self.port))

            print("connection established")
        except:
            QMessageBox.question(self, 'ERROR', "Connection Failed", QMessageBox.Yes )



    def recieveStream (self):
        print('waiting for connection')
        HOST = ''
        PORT = 4000
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        
        s.bind((HOST, PORT))
        print('Socket bind complete')
        s.listen(10)
        print('Socket now listening')
        
        conn, addr = s.accept()
        
        data = b'' ### CHANGED
        payload_size = struct.calcsize("L") ### CHANGED
        
        while True:
        
            # Retrieve message size
            while len(data) < payload_size:
                data += conn.recv(4096)
        
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED
             # Retrieve all data based on message size
            while len(data) < msg_size:
                data += conn.recv(4096)
        
            frame_data = data[:msg_size]
            data = data[msg_size:]
        
            # Extract frame
            frame = pickle.loads(frame_data)
        
            # Display
            cv2.imshow('frame', frame)
            cv2
            if cv2.waitKey(1) & 0xFF == ord('q'):
                s.close()
                print('socket closed')
                break
        

    def SendStream (self):
        try:
            print("stream")
            cap=cv2.VideoCapture(0)
            clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            clientsocket.connect((self.host,5000))
            print("connected stream")
            while True:
                ret,frame=cap.read()
                # Serialize frame
                data = pickle.dumps(frame)

                # Send message length first
                message_size = struct.pack("L", len(data)) ### CHANGED

                # Then data
                clientsocket.sendall(message_size + data)
            print("socket camera closed")
            clientsocket.close()
        except:
            QMessageBox.question(self, 'ERROR', "Connection Failed", QMessageBox.Yes )
            

    def checkLabel(self,data):
        if data == "l1":
            self.updateButtons(self.ui.lbl_1)
        elif  data == "l2":
            self.updateButtons(self.ui.lbl_2)
        elif  data == "l3":
            self.updateButtons(self.ui.lbl_3)
        elif  data == "l4":
            self.updateButtons(self.ui.lbl_4)
        elif data == "l5":
            self.updateButtons(self.ui.lbl_5)
        elif data == "l6":
            self.updateButtons(self.ui.lbl_6)
        elif data == "l7":
            self.updateButtons(self.ui.lbl_7)
        elif  data == "l8":
            self.updateButtons(self.ui.lbl_8)
        elif  data == "l9":
            self.updateButtons(self.ui.lbl_9)



    def updateButtons(self,label):
        label.setEnabled(False)
        label.setText(self.current)
 
        if(self.current == 'X'):    
            self.current ='O'
        else:
            self.current ='X'
        self.numOfClicks = self.numOfClicks +1
        if(self.numOfClicks > 4):
            self.checkForWin()
        print(self.numOfClicks)
        
        
    def disableAllLabels(self):
        self.ui.lbl_1.setEnabled(False)
        self.ui.lbl_2.setEnabled(False)
        self.ui.lbl_3.setEnabled(False)
        self.ui.lbl_4.setEnabled(False)
        self.ui.lbl_5.setEnabled(False)
        self.ui.lbl_6.setEnabled(False)
        self.ui.lbl_7.setEnabled(False)
        self.ui.lbl_8.setEnabled(False)
        self.ui.lbl_9.setEnabled(False)
        
        
    def enableAllLabels(self):
        self.ui.lbl_1.setEnabled(True)
        self.ui.lbl_2.setEnabled(True)
        self.ui.lbl_3.setEnabled(True)
        self.ui.lbl_4.setEnabled(True)
        self.ui.lbl_5.setEnabled(True)
        self.ui.lbl_6.setEnabled(True)
        self.ui.lbl_7.setEnabled(True)
        self.ui.lbl_8.setEnabled(True)
        self.ui.lbl_9.setEnabled(True)
        
        
    def clearAllLabels(self):
        self.ui.lbl_1.clear()
        self.ui.lbl_2.clear()
        self.ui.lbl_3.clear()
        self.ui.lbl_4.clear()
        self.ui.lbl_5.clear()
        self.ui.lbl_6.clear()   
        self.ui.lbl_7.clear()
        self.ui.lbl_8.clear()
        self.ui.lbl_9.clear()
        self.current = 'X'
        self.numOfClicks = 0
        self.isWiner = 0
        self.winer = ''


    def restartGame(self):
        self.disableAllLabels()
        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Restart Game?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.clearAllLabels()
            self.enableAllLabels()
        else:
            print('No clicked.')
        
        
    def checkForWin(self):
        if self.ui.lbl_1.text() ==  self.ui.lbl_2.text() and self.ui.lbl_3.text() ==  self.ui.lbl_2.text() != "":
            self.bgrb("one")
        elif self.ui.lbl_4.text() ==  self.ui.lbl_5.text() and self.ui.lbl_6.text() ==  self.ui.lbl_5.text() != "":
            self.bgrb("two")
        elif self.ui.lbl_7.text() ==  self.ui.lbl_8.text() and self.ui.lbl_9.text() == self.ui.lbl_8.text() != "": 
            self.bgrb("three")
        elif self.ui.lbl_1.text() ==  self.ui.lbl_5.text() and self.ui.lbl_9.text() == self.ui.lbl_5.text() != "":
            self.bgrb("four")
        elif self.ui.lbl_3.text() ==  self.ui.lbl_5.text() and self.ui.lbl_7.text() == self.ui.lbl_5.text() != "":
            self.bgrb("five")
        elif self.ui.lbl_1.text() ==  self.ui.lbl_4.text() and self.ui.lbl_7.text() ==  self.ui.lbl_4.text() != "": 
            self.bgrb("six")
        elif self.ui.lbl_2.text() ==  self.ui.lbl_5.text() and self.ui.lbl_8.text() == self.ui.lbl_5.text() != "":
            self.bgrb("seven")
        elif self.ui.lbl_3.text() ==  self.ui.lbl_6.text() and self.ui.lbl_9.text() == self.ui.lbl_6.text() != "":
            self.bgrb("eight")
            
        else:
            if(self.numOfClicks > 8):
                print('restart game') 
                QMessageBox.question(self, 'Bummer!!', "Its a DRAW !!!!!", QMessageBox.Yes )
                self.restartGame()
        
    def bgrb(self,text):
        self.isWiner = 1
        self.winer = self.current
        print("7sl restart bssbb or: "+text)
        QMessageBox.question(self, 'Winner', "Player" + self.winer +"Has Won", QMessageBox.Yes )

        self.restartGame()

    def showText1(self, event):
        QApplication.processEvents()
        self.ui.lbl_1.setText(self.current)
        message = "l1"
        self.mySocket.send(message.encode())
        self.toggle(self.ui.lbl_1)
        
    
    def showText2(self, event):
        QApplication.processEvents()
        self.ui.lbl_2.setText(self.current)
        message = "l2"
        self.mySocket.send(message.encode())

        self.toggle(self.ui.lbl_2)
        
    def showText3(self,event):
        QApplication.processEvents()
        self.ui.lbl_3.setText(self.current)
        message = "l3"
        self.mySocket.send(message.encode())

        self.toggle(self.ui.lbl_3)
        
    def showText4(self,event):
        QApplication.processEvents()
        self.ui.lbl_4.setText(self.current)
        message = "l4"
        self.mySocket.send(message.encode())

        self.toggle(self.ui.lbl_4)
        
    def showText5(self,event):
        QApplication.processEvents()
        self.ui.lbl_5.setText(self.current)
        message = "l5"
        self.mySocket.send(message.encode())

        self.toggle(self.ui.lbl_5)
        
    def showText6(self,event):
        QApplication.processEvents()
        self.ui.lbl_6.setText(self.current)
        message = "l6"
        self.mySocket.send(message.encode())

        self.toggle(self.ui.lbl_6)

    def showText7(self,event):
        QApplication.processEvents()
        self.ui.lbl_7.setText(self.current)
        message = "l7"
        self.mySocket.send(message.encode())
        self.toggle(self.ui.lbl_7)
        
    def showText8(self,event):
        QApplication.processEvents()
        self.ui.lbl_8.setText(self.current)
        message = "l8"
        self.mySocket.send(message.encode())
        self.toggle(self.ui.lbl_8)
        
    def showText9(self,event):
        QApplication.processEvents()
        self.ui.lbl_9.setText(self.current)
        message = "l9"
        self.mySocket.send(message.encode())

        self.toggle(self.ui.lbl_9)
       
    def Connect(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        # text1 , result = QInputDialog.getText (self, 'Info' ,"Enter IP" )
        # if result== True:
        #     self.ui.ln_IP.setText(str(text1))

        #     text2 , result = QInputDialog.getText (self, 'Info' ,"Enter port " )
        #     if result== True:
        #         self.ui.ln_Port.setText(str(text2))
        #         # self.style()
        #         #self.connection(str(text1),int(text2))
        #         self.ui.ln_name2.setText(str(self.ui.ln_name.text()))
                

               # self.ui=form2()
               # self.ui.setupUi(self)
#               app = QtWidgets.QApplication(sys.argv)
 #               self.close()
  #              application = p2()
   #             application.show()
    #            sys.exit(app.exec_())
    
    def Game (self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.clearAllLabels()
        self.enableAllLabels()
        self.ui.ln_name2.setText(self.ui.ln_name.text())

        
        
    def mousePressEvent(self, event):
       self.x=event.pos().x()
       self.y=event.pos().y()


        
        
    def RecieveFile (self):
        try:
            print("butoon recieved clicked")
            soc = socket.socket()
            soc.connect((self.host,8080))
            print("socketconnected")
            with soc,open("file",'wb') as file:
                while True:
                    recvfile = soc.recv(4096)
                    print(recvfile)
                    if not recvfile: break
                    file.write(recvfile)
            print("File has been received.")
            soc.close()
            try:
                image = mpimg.imread("file")
                plt.imshow(image)
                plt.show()

            except:
                # # cap = cv2.VideoCapture(0)
                capture = cv2.VideoCapture('file')
                while(True):
                    ret, frame = capture.read()   
                    cv2.imshow('video', frame)
                    if cv2.waitKey(27) & 0xFF == ord('q'):
                        break

                # When everything done, release the capture
                capture.release()
                cv2.destroyAllWindows()
        except:
                QMessageBox.question(self, 'ERROR', "Connection Failed", QMessageBox.Yes )

        

        # self.filename, _filter=QFileDialog.getOpenFileName(self,"open file"," ","Image File(*.png *.jpg *.jpeg *.bmp)")
        # if self.filename:
        #     #imagePath = self.filename 
    def Sendfile (self):
        try:
            self.filename, _filter=QFileDialog.getOpenFileName(self,"open file"," ","Image File(*.*)")
            if self.filename:
                soc = socket.socket()
                soc.bind(('',8080))
                soc.listen(1)
                
                print('waiting for connection...')
                with soc:
                    con,addr = soc.accept()
                    print('server connected to',addr)
                    with con:
                        filename =self.filename
                        print(filename)       
                        with open(filename, 'rb') as file:
                            sendfile = file.read()
                        con.sendall(sendfile)
                        print('file sent')
                soc.close()
        except:
                QMessageBox.question(self, 'ERROR', "Connection Refused", QMessageBox.Yes )

    def connection (self , Ip , portnumber):
            cap=cv2.VideoCapture(0)
            clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            clientsocket.connect((Ip,portnumber))
            
            while True:
                ret,frame=cap.read()
                # Serialize frame
                data = pickle.dumps(frame)
                
                # Send message length first
                message_size = struct.pack("L", len(data)) ### CHANGED
                
                # Then data
                clientsocket.sendall(message_size + data)
                QApplication.processEvents()
        




    # def style (self):
    #     self.ui.ln_Port.show()
    #     self.ui.lbl_Port.show()
    #     self.ui.ln_IP.show()
    #     self.ui.lbl_IP.show()
    #     self.ui.btn_Game.show()
    #     self.ui.btn_Sendfile.show()
    #     self.ui.btn_Startstreaming.show()            
            


def main(): 
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
