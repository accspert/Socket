
import socket
from asyncio import events
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QWidget
)
from PyQt5 import uic
from ErrorLogger import *
import traceback

def handle_error(error):
    """Handles exceptions by logging their tracebacks and displaying a critical QMessageBox."""
    ErrorLogger.WriteError(traceback.format_exc())
    QtWidgets.QMessageBox.critical(None, "Exception raised", format(error))

class EgonSocket(socket.socket):

    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
        socket.socket.__init__(self, family, type, proto, fileno)

        self.hostname = None
        self.port = None
        self.filename = None
        
    def getsockname(self):
        return super().getsockname()

    # def recv(self):
        
    #     filename = "C:/Users/Egon/Pictures/received.pptx"
    #     file = open(filename, 'wb')
    #     file_data = self.recv(1024)
    #     file.write(file_data)
    #     file.close()
    #     handle_error('File has been received')
    
    def client_connect(self, host, port):

        self.connect((host, port))

class MainForm(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.hostname = None
        self.port = None

        uic.loadUi(r"egon_client.ui", self)
        self.labelConnected.setVisible(False)

        self.egon_socket = EgonSocket()

        self.pushButtonConnect.clicked.connect(self.connect)

    def connect(self):
        self.egon_socket.client_connect(self.lineEditHost.text(), int(self.lineEditPort.text()))
        self.socket_info = self.egon_socket.getsockname()
        self.hostname, self.port = self.socket_info
        
        self.labelSocketInfo.setText('Your host is: ' + str(self.hostname) + ' Port is: ' + str(self.port) )
        self.pushButtonConnect.setVisible(False)
        self.labelConnected.setVisible(True)
        
        while True:
            file_data = self.egon_socket.recv(1024)

            if file_data:
                
                filename = "C:/Users/Egon/Pictures/received.pptx"
                file = open(filename, 'wb')
                file.write(file_data)
                file.close()
                handle_error('File has been received')

def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()