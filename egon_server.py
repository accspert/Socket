import socket
import sys
import time

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QWidget
)
from PyQt5 import uic
import threading
from ErrorLogger import *
import traceback

def handle_error(error):
    """Handles exceptions by logging their tracebacks and displaying a critical QMessageBox."""
    ErrorLogger.WriteError(traceback.format_exc())
    QtWidgets.QMessageBox.critical(None, "Exception raised", format(error))

class EgonSocket(socket.socket):

    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):

        socket.socket.__init__(self, family, type, proto, fileno)
        
        self.filename = None
        self.conn = None
        self.add = None
 
    @property
    def get_file(self):
        self.filename, extension = QFileDialog.getOpenFileName(QWidget(), 'Choose a file', '',
                                                      'Files (*.*)')
        return self.filename

    def send_my_file(self):    
        
        try:
            file = open(self.filename, 'rb')
            file_data = file.read(1024)
            self.conn.send(file_data)
            self.close()
        except Exception as e:
            handle_error(e)

    def server_connect(self):
        self.bind((socket.gethostname(), 9879))
        self.listen(1)
    def accept_mo(self):
        self.conn, self.addr = self.accept()

class MainForm(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.hostname = None
        self.port = None
        self.conn = None
        self.add = None

        uic.loadUi(r"egon_server.ui", self)
        self.labelConnected.setVisible(False)
        self.labelAccepting.setVisible(False)

        self.egon_socket = EgonSocket()

        self.pushButtonConnect.clicked.connect(self.connect)
        self.pushButtonChooseFile.clicked.connect(self.get_file)
        self.pushButtonSendFile.clicked.connect(self.send_file)
        self.pushButtonAccept.clicked.connect(self.accept)
    def closeEvent(self, e):
        self.egon_socket.close()
        self.thread
    def accept(self):
        self.pushButtonAccept.setVisible(False)
        self.labelAccepting.setVisible(True)
        self.thread = threading.Thread(target=self.egon_socket.accept_mo())
        self.thread.start()

    def connect(self):

        self.egon_socket.server_connect()
        self.socket_info = self.egon_socket.getsockname()
        self.hostname, self.port = self.socket_info
        
        self.labelSocketInfo.setText('Your host is: ' + str(self.hostname) + ' Port is: ' + str(self.port) )
        self.pushButtonConnect.setVisible(False)
        self.labelConnected.setVisible(True)

    def get_file(self):
        self.filename = self.egon_socket.get_file
        self.labelFile.setText(str(self.filename))
    def send_file(self):
        self.egon_socket.send_my_file()


def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()